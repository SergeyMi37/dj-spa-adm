<template>
  <div class="container">
    <div class="mb-3">
      <h5><i class="fas fa-wind"></i> AirFlow - Управление DAG'ами</h5>
      <hr>
      
      <!-- Форма для создания/редактирования DAG -->
      <div class="card mb-4">
        <div class="card-header">
          <h6 class="mb-0">Управление DAG'ами</h6>
        </div>
        <div class="card-body">
          <form @submit.prevent="createDag">
            <div class="row">
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="dagId" class="form-label">DAG ID</label>
                  <input
                    type="text"
                    id="dagId"
                    v-model="newDag.dag_id"
                    class="form-control"
                    placeholder="Введите ID DAG'а"
                    required
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="schedule" class="form-label">Расписание</label>
                  <select id="schedule" v-model="newDag.schedule" class="form-control">
                    <option value="">Выберите расписание</option>
                    <option value="@daily">Ежедневно</option>
                    <option value="@weekly">Еженедельно</option>
                    <option value="@monthly">Ежемесячно</option>
                    <option value="0 * * * *">Каждый час</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="mb-3">
              <label for="description" class="form-label">Описание</label>
              <textarea
                id="description"
                v-model="newDag.description"
                class="form-control"
                rows="2"
                placeholder="Описание DAG'а"
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Создается...' : 'Создать DAG' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Список DAG'ов -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h6 class="mb-0">Список DAG'ов</h6>
          <button @click="loadDags" class="btn btn-sm btn-outline-secondary" :disabled="loading">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> Обновить
          </button>
        </div>
        <div class="card-body">
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          
          <div v-if="dags.length === 0 && !loading" class="text-center text-muted py-4">
            <i class="fas fa-inbox fa-3x mb-3"></i>
            <p>DAG'и не найдены</p>
          </div>
          
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-2">Загрузка DAG'ов...</p>
          </div>
          
          <div v-if="dags.length > 0" class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>DAG ID</th>
                  <th>Состояние</th>
                  <th>Последний запуск</th>
                  <th>Следующий запуск</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="dag in dags" :key="dag.dag_id">
                  <td>
                    <strong>{{ dag.dag_id }}</strong>
                    <br>
                    <small class="text-muted">{{ dag.description || 'Без описания' }}</small>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadge(dag.state)">
                      {{ getStatusText(dag.state) }}
                    </span>
                  </td>
                  <td>
                    <small>{{ formatDate(dag.last_run) }}</small>
                  </td>
                  <td>
                    <small>{{ formatDate(dag.next_run) }}</small>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <button 
                        @click="triggerDag(dag.dag_id)" 
                        class="btn btn-outline-primary"
                        title="Запустить DAG"
                        :disabled="loading"
                      >
                        <i class="fas fa-play"></i>
                      </button>
                      <button 
                        @click="pauseDag(dag.dag_id)" 
                        class="btn btn-outline-warning"
                        :title="dag.is_paused ? 'Возобновить' : 'Приостановить'"
                        :disabled="loading"
                      >
                        <i :class="dag.is_paused ? 'fa-play' : 'fa-pause'"></i>
                      </button>
                      <button 
                        @click="deleteDag(dag.dag_id)" 
                        class="btn btn-outline-danger"
                        title="Удалить DAG"
                        :disabled="loading"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Airflow',
  data() {
    return {
      dags: [],
      loading: false,
      error: null,
      newDag: {
        dag_id: '',
        schedule: '',
        description: ''
      }
    };
  },
  mounted() {
    this.loadDags();
  },
  methods: {
    async loadDags() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('/api/airflow/dags/', {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        
        this.dags = response.data.dags || [];
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка загрузки DAG\'ов';
        this.dags = [];
      } finally {
        this.loading = false;
      }
    },

    async createDag() {
      if (!this.newDag.dag_id.trim()) {
        this.error = 'Введите ID DAG\'а';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post('/api/airflow/dags/', this.newDag, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        // Очищаем форму
        this.newDag = {
          dag_id: '',
          schedule: '',
          description: ''
        };

        // Обновляем список DAG'ов
        await this.loadDags();
        
        alert('DAG успешно создан');
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка создания DAG\'а';
      } finally {
        this.loading = false;
      }
    },

    async triggerDag(dagId) {
      if (!confirm(`Запустить DAG "${dagId}"?`)) return;

      this.loading = true;
      try {
        await axios.post(`/api/airflow/dags/${dagId}/trigger/`, {}, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        
        alert('DAG запущен');
        await this.loadDags();
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка запуска DAG\'а';
      } finally {
        this.loading = false;
      }
    },

    async pauseDag(dagId) {
      const action = 'pause';
      if (!confirm(`${action === 'pause' ? 'Приостановить' : 'Возобновить'} DAG "${dagId}"?`)) return;

      this.loading = true;
      try {
        await axios.post(`/api/airflow/dags/${dagId}/${action}/`, {}, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        
        await this.loadDags();
      } catch (err) {
        this.error = err.response?.data?.error || `Ошибка ${action === 'pause' ? 'приостановки' : 'возобновления'} DAG\'а`;
      } finally {
        this.loading = false;
      }
    },

    async deleteDag(dagId) {
      if (!confirm(`Удалить DAG "${dagId}"? Это действие нельзя отменить.`)) return;

      this.loading = true;
      try {
        await axios.delete(`/api/airflow/dags/${dagId}/`, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        
        await this.loadDags();
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка удаления DAG\'а';
      } finally {
        this.loading = false;
      }
    },

    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    getStatusBadge(state) {
      const badges = {
        'running': 'bg-success',
        'paused': 'bg-warning',
        'failed': 'bg-danger',
        'success': 'bg-info',
        'queued': 'bg-secondary'
      };
      return badges[state] || 'bg-secondary';
    },

    getStatusText(state) {
      const texts = {
        'running': 'Выполняется',
        'paused': 'Приостановлен',
        'failed': 'Ошибка',
        'success': 'Успешно',
        'queued': 'В очереди'
      };
      return texts[state] || state;
    },

    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleString('ru-RU');
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.card {
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.badge {
  font-size: 0.75em;
}

.text-muted {
  color: #6c757d !important;
}

.alert {
  margin-bottom: 1rem;
}

.spinner-border {
  width: 2rem;
  height: 2rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 10px;
  }
  
  .card-body {
    padding: 1rem 0.5rem;
  }
  
  .btn-group {
    flex-direction: column;
  }
  
  .btn-group .btn {
    margin-bottom: 2px;
  }
}
</style>