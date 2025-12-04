<template>
  <div class="container">
    <!-- Модальное окно настроек подключения к RabbitMQ -->
    <div v-if="showConnectionSettings" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0,0,0,0.5);" @click="closeModal">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-envelope"></i>
              Настройки подключения к RabbitMQ
            </h5>
            <button
              @click.stop="closeModal"
              type="button"
              class="btn-close"
              aria-label="Закрыть"
            ></button>
          </div>
          <div class="modal-body">
            <div v-if="modalError" class="alert alert-danger mb-3">
              {{ modalError }}
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="rabbitmqHost" class="form-label">Хост:</label>
                <input
                  id="rabbitmqHost"
                  v-model="connectionSettings.host"
                  type="text"
                  class="form-control"
                  placeholder="localhost"
                >
              </div>
              <div class="col-md-6">
                <label for="rabbitmqPort" class="form-label">Порт:</label>
                <input
                  id="rabbitmqPort"
                  v-model="connectionSettings.port"
                  type="number"
                  class="form-control"
                  placeholder="5672"
                >
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="rabbitmqUsername" class="form-label">Пользователь:</label>
                <input
                  id="rabbitmqUsername"
                  v-model="connectionSettings.username"
                  type="text"
                  class="form-control"
                  placeholder="guest"
                >
              </div>
              <div class="col-md-6">
                <label for="rabbitmqPassword" class="form-label">Пароль:</label>
                <div class="input-group">
                  <input
                    id="rabbitmqPassword"
                    v-model="connectionSettings.password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    placeholder="guest"
                  >
                  <div class="input-group-append">
                    <button
                      @click="showPassword = !showPassword"
                      class="btn btn-outline-secondary"
                      type="button"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="rabbitmqVhost" class="form-label">Virtual Host:</label>
                <input
                  id="rabbitmqVhost"
                  v-model="connectionSettings.vhost"
                  type="text"
                  class="form-control"
                  placeholder="/"
                >
              </div>
              <div class="col-md-6 d-flex align-items-end">
                <button @click="testConnection" class="btn btn-info mr-2" :disabled="loading">
                  <i class="fas fa-plug"></i>
                  Тест подключения
                </button>
                <button @click="saveConnection" class="btn btn-success">
                  <i class="fas fa-save"></i>
                  Сохранить
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" type="button" class="btn btn-secondary">
              <i class="fas fa-times"></i>
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Основная область управления RabbitMQ -->
    <div class="mb-3">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>
          <i class="fas fa-envelope text-primary"></i>
          Брокер сообщений – RabbitMQ
        </h4>
        <div class="d-flex gap-2">
          <button
            @click="showConnectionSettings = true; modalError = null"
            class="btn btn-outline-primary btn-sm"
          >
            <i class="fas fa-cog"></i>
            Настройки подключения
          </button>
          <button @click="loadQueues" class="btn btn-outline-secondary btn-sm" :disabled="loading">
            <i class="fas fa-sync"></i>
            Обновить
          </button>
        </div>
      </div>

      <!-- Панель создания новой очереди -->
      <div class="card mb-3">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-plus"></i>
            Создать новую очередь
          </h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <label for="newQueueName" class="form-label">Имя очереди:</label>
              <input
                id="newQueueName"
                v-model="newQueue.name"
                type="text"
                class="form-control"
                placeholder="queue_name"
              >
            </div>
            <div class="col-md-3">
              <label for="newQueueDurable" class="form-label">Durable:</label>
              <select id="newQueueDurable" v-model="newQueue.durable" class="form-control">
                <option :value="true">Да</option>
                <option :value="false">Нет</option>
              </select>
            </div>
            <div class="col-md-3">
              <label for="newQueueAutoDelete" class="form-label">Auto Delete:</label>
              <select id="newQueueAutoDelete" v-model="newQueue.autoDelete" class="form-control">
                <option :value="false">Нет</option>
                <option :value="true">Да</option>
              </select>
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button @click="createQueue" class="btn btn-success" :disabled="loading">
                <i class="fas fa-plus"></i>
                Создать
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Панель отправки сообщения -->
      <div class="card mb-3">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-paper-plane"></i>
            Отправить сообщение
          </h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <label for="messageQueue" class="form-label">Очередь:</label>
              <select id="messageQueue" v-model="message.queue" class="form-control">
                <option value="">Выберите очередь...</option>
                <option
                  v-for="queue in queues"
                  :key="queue.name"
                  :value="queue.name"
                >
                  {{ queue.name }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <label for="messageRoutingKey" class="form-label">Routing Key:</label>
              <input
                id="messageRoutingKey"
                v-model="message.routingKey"
                type="text"
                class="form-control"
                placeholder="routing.key"
              >
            </div>
            <div class="col-md-4">
              <label for="messageContent" class="form-label">Сообщение:</label>
              <input
                id="messageContent"
                v-model="message.content"
                type="text"
                class="form-control"
                placeholder="Текст сообщения"
              >
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button @click="sendMessage" class="btn btn-primary" :disabled="loading">
                <i class="fas fa-paper-plane"></i>
                Отправить
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Список очередей -->
      <div class="card">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-list"></i>
            Очереди ({{ queues.length }})
          </h6>
        </div>
        <div class="card-body">
          <div v-if="queues.length === 0 && !loading" class="text-center text-muted py-4">
            <i class="fas fa-inbox fa-3x mb-3"></i>
            <p>Очередей не найдено</p>
            <button @click="loadQueues" class="btn btn-outline-primary btn-sm">
              <i class="fas fa-sync"></i>
              Обновить
            </button>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Имя очереди</th>
                  <th>Сообщений</th>
                  <th>Потребители</th>
                  <th>Durable</th>
                  <th>Auto Delete</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="queue in queues" :key="queue.name">
                  <td>
                    <strong>{{ queue.name }}</strong>
                  </td>
                  <td>
                    <span class="badge badge-info">{{ queue.messages || 0 }}</span>
                  </td>
                  <td>
                    <span class="badge badge-success">{{ queue.consumers || 0 }}</span>
                  </td>
                  <td>
                    <span :class="queue.durable ? 'badge badge-success' : 'badge badge-secondary'">
                      {{ queue.durable ? 'Да' : 'Нет' }}
                    </span>
                  </td>
                  <td>
                    <span :class="queue.auto_delete ? 'badge badge-warning' : 'badge badge-secondary'">
                      {{ queue.auto_delete ? 'Да' : 'Нет' }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <button
                        @click="viewQueueMessages(queue.name)"
                        class="btn btn-outline-info"
                        title="Просмотреть сообщения"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button
                        @click="purgeQueue(queue.name)"
                        class="btn btn-outline-warning"
                        title="Очистить очередь"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                      <button
                        @click="deleteQueue(queue.name)"
                        class="btn btn-outline-danger"
                        title="Удалить очередь"
                      >
                        <i class="fas fa-times"></i>
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

    <!-- Сообщения об ошибках -->
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- Сообщения об успехе -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RabbitMQ',
  data() {
    return {
      loading: false,
      error: null,
      successMessage: null,
      
      // Настройки подключения
      showConnectionSettings: false,
      showPassword: false,
      connectionSettings: {
        host: 'localhost',
        port: 5672,
        username: 'guest',
        password: 'guest',
        vhost: '/'
      },
      modalError: null,
      
      // Данные очередей
      queues: [],
      
      // Создание новой очереди
      newQueue: {
        name: '',
        durable: true,
        autoDelete: false
      },
      
      // Отправка сообщения
      message: {
        queue: '',
        routingKey: '',
        content: ''
      }
    };
  },
  mounted() {
    this.loadQueues();
    this.loadConnectionSettings();
  },
  methods: {
    async loadQueues() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get('/api/rabbitmq/queues/', {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.queues = response.data.queues || [];
        this.showSuccess('Список очередей обновлен');
      } catch (err) {
        this.error = 'Ошибка загрузки очередей: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async testConnection() {
      this.modalError = null;
      
      if (!this.connectionSettings.host || !this.connectionSettings.username) {
        this.modalError = 'Заполните хост и имя пользователя';
        return;
      }

      this.loading = true;
      this.modalError = null;

      try {
        const response = await axios.post('/api/rabbitmq/test-connection/', {
          connection: this.connectionSettings
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (response.data.success) {
          alert('Подключение к RabbitMQ успешно!');
          this.closeModal();
          this.loadQueues();
        } else {
          this.modalError = 'Ошибка подключения: ' + (response.data.error || 'Неизвестная ошибка');
        }
      } catch (err) {
        this.modalError = 'Ошибка тестирования подключения: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async saveConnection() {
      this.modalError = null;
      
      if (!this.connectionSettings.host) {
        this.modalError = 'Укажите хост RabbitMQ';
        return;
      }

      try {
        localStorage.setItem('rabbitmq_connection', JSON.stringify(this.connectionSettings));
        this.showSuccess('Настройки подключения сохранены');
        this.closeModal();
        this.loadQueues();
      } catch (err) {
        this.modalError = 'Ошибка сохранения настроек: ' + err.message;
      }
    },

    loadConnectionSettings() {
      try {
        const saved = localStorage.getItem('rabbitmq_connection');
        if (saved) {
          this.connectionSettings = JSON.parse(saved);
        }
      } catch (e) {
        console.warn('Не удалось загрузить настройки подключения:', e);
      }
    },

    async createQueue() {
      if (!this.newQueue.name.trim()) {
        this.showError('Укажите имя очереди');
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post('/api/rabbitmq/queues/', {
          name: this.newQueue.name,
          durable: this.newQueue.durable,
          auto_delete: this.newQueue.autoDelete
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.showSuccess('Очередь создана успешно');
        this.newQueue = { name: '', durable: true, autoDelete: false };
        this.loadQueues();
      } catch (err) {
        this.error = 'Ошибка создания очереди: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async sendMessage() {
      if (!this.message.queue || !this.message.content.trim()) {
        this.showError('Укажите очередь и содержимое сообщения');
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post('/api/rabbitmq/messages/', {
          queue: this.message.queue,
          routing_key: this.message.routingKey,
          content: this.message.content
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.showSuccess('Сообщение отправлено успешно');
        this.message = { queue: '', routingKey: '', content: '' };
        this.loadQueues();
      } catch (err) {
        this.error = 'Ошибка отправки сообщения: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async viewQueueMessages(queueName) {
      try {
        const response = await axios.get(`/api/rabbitmq/queues/${queueName}/messages/`, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        const messages = response.data.messages || [];
        if (messages.length === 0) {
          alert(`В очереди "${queueName}" нет сообщений`);
        } else {
          alert(`Сообщения в очереди "${queueName}":\n\n${messages.map((msg, index) => `${index + 1}. ${msg.content || msg}`).join('\n')}`);
        }
      } catch (err) {
        this.error = 'Ошибка получения сообщений: ' + (err.response?.data?.error || err.message);
      }
    },

    async purgeQueue(queueName) {
      if (!confirm(`Вы уверены, что хотите очистить очередь "${queueName}"?`)) return;

      try {
        const response = await axios.delete(`/api/rabbitmq/queues/${queueName}/purge/`, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.showSuccess(`Очередь "${queueName}" очищена`);
        this.loadQueues();
      } catch (err) {
        this.error = 'Ошибка очистки очереди: ' + (err.response?.data?.error || err.message);
      }
    },

    async deleteQueue(queueName) {
      if (!confirm(`Вы уверены, что хотите удалить очередь "${queueName}"?`)) return;

      try {
        const response = await axios.delete(`/api/rabbitmq/queues/${queueName}/`, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.showSuccess(`Очередь "${queueName}" удалена`);
        this.loadQueues();
      } catch (err) {
        this.error = 'Ошибка удаления очереди: ' + (err.response?.data?.error || err.message);
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

    showError(message) {
      this.error = message;
      this.successMessage = null;
      setTimeout(() => {
        this.error = null;
      }, 5000);
    },

    showSuccess(message) {
      this.successMessage = message;
      this.error = null;
      setTimeout(() => {
        this.successMessage = null;
      }, 3000);
    },

    closeModal() {
      this.showConnectionSettings = false;
      this.modalError = null;
      this.error = null;
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.badge-info {
  background-color: #17a2b8;
  color: white;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: black;
}

.badge-secondary {
  background-color: #6c757d;
  color: white;
}

.btn:disabled {
  cursor: not-allowed;
}

.text-muted {
  color: #6c757d !important;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.form-control {
  font-size: 14px;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 14px;
}

@media (max-width: 768px) {
  .d-flex.justify-content-between.align-items-center {
    flex-direction: column;
    gap: 10px;
  }
  
  .d-flex.gap-2 {
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }
  
  .form-control {
    width: 100% !important;
  }
  
  .btn-group {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
}

/* Стили для активного состояния кнопок */
.btn:active {
  color: #e9ecef !important;
}

.btn-outline-primary:active {
  color: #f8f9fa !important;
}

.btn-outline-secondary:active {
  color: #f8f9fa !important;
}
</style>