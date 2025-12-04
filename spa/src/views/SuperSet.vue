<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-chart-bar"></i> Apache SuperSet</h2>
          <div class="btn-group" role="group">
            <button 
              @click="refreshDashboard" 
              class="btn btn-outline-primary btn-sm"
              :disabled="loading"
            >
              <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
              Обновить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Информационная панель -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-info-circle text-info"></i>
              О SuperSet
            </h5>
            <p class="card-text">
              Apache SuperSet - это современная платформа для бизнес-аналитики и визуализации данных. 
              Она предоставляет возможности для создания интерактивных дашбордов, отчетов и анализа данных.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации SuperSet -->
      <div class="col-md-3">
        <div class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-tasks"></i>
              Разделы
            </h6>
          </div>
          <div class="list-group list-group-flush">
            <button 
              @click="activeSection = 'dashboard'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'dashboard' }]"
            >
              <i class="fas fa-chart-line me-2"></i>
              Дашборды
            </button>
            <button 
              @click="activeSection = 'charts'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'charts' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Графики
            </button>
            <button 
              @click="activeSection = 'queries'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'queries' }]"
            >
              <i class="fas fa-database me-2"></i>
              SQL запросы
            </button>
            <button 
              @click="activeSection = 'sources'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'sources' }]"
            >
              <i class="fas fa-plug me-2"></i>
              Источники данных
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Дашборды -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Дашборды
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="dashboard in dashboards" :key="dashboard.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">{{ dashboard.title }}</h6>
                    <p class="card-text text-muted small">{{ dashboard.description }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">{{ dashboard.charts_count }} графиков</small>
                      <button 
                        @click="openDashboard(dashboard.id)"
                        class="btn btn-primary btn-sm"
                      >
                        Открыть
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="dashboards.length === 0" class="text-center py-4">
              <i class="fas fa-chart-line fa-3x text-muted mb-3"></i>
              <p class="text-muted">Дашборды не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Графики -->
        <div v-if="activeSection === 'charts'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Графики
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3" v-for="chart in charts" :key="chart.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">{{ chart.title }}</h6>
                    <p class="card-text">
                      <small class="text-muted">
                        <i class="fas fa-layer-group me-1"></i>
                        {{ chart.chart_type }}
                      </small>
                    </p>
                    <button 
                      @click="openChart(chart.id)"
                      class="btn btn-outline-primary btn-sm"
                    >
                      Посмотреть
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="charts.length === 0" class="text-center py-4">
              <i class="fas fa-chart-bar fa-3x text-muted mb-3"></i>
              <p class="text-muted">Графики не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел SQL запросы -->
        <div v-if="activeSection === 'queries'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-database"></i>
              SQL запросы
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <button 
                @click="createNewQuery"
                class="btn btn-success"
              >
                <i class="fas fa-plus"></i>
                Новый запрос
              </button>
            </div>
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>База данных</th>
                    <th>Последнее выполнение</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="query in sqlQueries" :key="query.id">
                    <td>{{ query.title }}</td>
                    <td>
                      <span class="badge bg-info">{{ query.database }}</span>
                    </td>
                    <td>
                      <small>{{ formatDate(query.last_run) }}</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="runQuery(query.id)"
                          class="btn btn-outline-primary"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                        <button 
                          @click="editQuery(query.id)"
                          class="btn btn-outline-secondary"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="sqlQueries.length === 0" class="text-center py-4">
              <i class="fas fa-database fa-3x text-muted mb-3"></i>
              <p class="text-muted">Запросы не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Источники данных -->
        <div v-if="activeSection === 'sources'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-plug"></i>
              Источники данных
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="source in dataSources" :key="source.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i :class="getSourceIcon(source.type)"></i>
                      {{ source.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ source.description }}</small>
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                      <span 
                        :class="['badge', source.status === 'connected' ? 'bg-success' : 'bg-danger']"
                      >
                        {{ source.status === 'connected' ? 'Подключен' : 'Отключен' }}
                      </span>
                      <small class="text-muted">{{ source.tables_count }} таблиц</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="dataSources.length === 0" class="text-center py-4">
              <i class="fas fa-plug fa-3x text-muted mb-3"></i>
              <p class="text-muted">Источники данных не найдены</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Ошибки и уведомления -->
    <div v-if="error" class="row mt-3">
      <div class="col-12">
        <div class="alert alert-danger" role="alert">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SuperSet',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      dashboards: [
        {
          id: 1,
          title: 'Продажи по регионам',
          description: 'Анализ продаж по различным регионам',
          charts_count: 8
        },
        {
          id: 2,
          title: 'Финансовые показатели',
          description: 'Основные финансовые метрики компании',
          charts_count: 12
        },
        {
          id: 3,
          title: 'Пользовательская активность',
          description: 'Статистика использования системы',
          charts_count: 6
        }
      ],
      charts: [
        {
          id: 1,
          title: 'Динамика продаж',
          chart_type: 'Line Chart'
        },
        {
          id: 2,
          title: 'Распределение по категориям',
          chart_type: 'Pie Chart'
        },
        {
          id: 3,
          title: 'Топ продуктов',
          chart_type: 'Bar Chart'
        }
      ],
      sqlQueries: [
        {
          id: 1,
          title: 'Продажи за месяц',
          database: 'main_db',
          last_run: new Date('2024-01-15')
        },
        {
          id: 2,
          title: 'Количество пользователей',
          database: 'analytics_db',
          last_run: new Date('2024-01-14')
        }
      ],
      dataSources: [
        {
          id: 1,
          name: 'PostgreSQL',
          type: 'postgres',
          description: 'Основная база данных приложения',
          status: 'connected',
          tables_count: 45
        },
        {
          id: 2,
          name: 'MySQL Warehouse',
          type: 'mysql',
          description: 'Хранилище аналитических данных',
          status: 'connected',
          tables_count: 23
        },
        {
          id: 3,
          name: 'Redis Cache',
          type: 'redis',
          description: 'Кэш данных',
          status: 'disconnected',
          tables_count: 0
        }
      ]
    };
  },
  methods: {
    async refreshDashboard() {
      this.loading = true;
      this.error = null;
      
      try {
        // Имитация обновления данных
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // В реальном приложении здесь был бы API вызов
        console.log('Dashboard refreshed');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    openDashboard(dashboardId) {
      // В реальном приложении здесь была бы навигация к дашборду
      console.log(`Opening dashboard ${dashboardId}`);
      alert(`Открытие дашборда ${dashboardId} (заглушка)`);
    },

    openChart(chartId) {
      // В реальном приложении здесь была бы навигация к графику
      console.log(`Opening chart ${chartId}`);
      alert(`Открытие графика ${chartId} (заглушка)`);
    },

    createNewQuery() {
      // В реальном приложении здесь был бы вызов редактора запросов
      console.log('Creating new query');
      alert('Создание нового запроса (заглушка)');
    },

    runQuery(queryId) {
      // В реальном приложении здесь был бы запуск запроса
      console.log(`Running query ${queryId}`);
      alert(`Выполнение запроса ${queryId} (заглушка)`);
    },

    editQuery(queryId) {
      // В реальном приложении здесь было бы открытие редактора запросов
      console.log(`Editing query ${queryId}`);
      alert(`Редактирование запроса ${queryId} (заглушка)`);
    },

    getSourceIcon(type) {
      const icons = {
        postgres: 'fas fa-database text-primary',
        mysql: 'fas fa-database text-info',
        redis: 'fas fa-memory text-warning',
        mongodb: 'fas fa-leaf text-success',
        default: 'fas fa-plug text-secondary'
      };
      return icons[type] || icons.default;
    },

    formatDate(date) {
      if (!date) return 'Не выполнялся';
      
      const d = new Date(date);
      return d.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
  mounted() {
    // Загрузка начальных данных при инициализации компонента
    console.log('SuperSet component mounted');
  }
};
</script>

<style scoped>
.container {
  max-width: 1400px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.list-group-item.active {
  background-color: #007bff;
  border-color: #007bff;
}

.list-group-item-action:hover {
  background-color: #f8f9fa;
}

.badge {
  font-size: 0.75em;
}

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.fas.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 10px;
  }
  
  .btn-group {
    flex-direction: column;
  }
  
  .btn-group .btn {
    margin-bottom: 5px;
  }
}
</style>