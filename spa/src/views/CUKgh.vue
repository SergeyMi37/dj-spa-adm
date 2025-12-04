<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-tachometer-alt"></i> ЦУ КГХ</h2>
          <div class="btn-group" role="group">
            <button 
              @click="refreshData" 
              class="btn btn-outline-primary btn-sm"
              :disabled="loading"
            >
              <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
              Обновить
            </button>
            <button 
              @click="generateReport" 
              class="btn btn-outline-success btn-sm"
            >
              <i class="fas fa-file-alt"></i>
              Отчет
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Панель мониторинга -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">
              <i class="fas fa-dashboard text-info"></i>
              Центр управления жилищно-коммунальным хозяйством
            </h5>
            <p class="card-text">
              ЦУ КГХ - это единая система мониторинга и управления жилищно-коммунальными 
              услугами региона, обеспечивающая контроль качества предоставляемых услуг, 
              мониторинг инфраструктуры и эффективное управление ресурсами.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Ключевые показатели -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ stats.totalComplaints }}</h3>
                <p class="mb-0">Всего обращений</p>
              </div>
              <i class="fas fa-clipboard-list fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ stats.resolvedToday }}</h3>
                <p class="mb-0">Решено сегодня</p>
              </div>
              <i class="fas fa-check-circle fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ stats.pendingComplaints }}</h3>
                <p class="mb-0">В обработке</p>
              </div>
              <i class="fas fa-clock fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ stats.satisfaction }}%</h3>
                <p class="mb-0">Удовлетворенность</p>
              </div>
              <i class="fas fa-smile fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации ЦУ КГХ -->
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
              Общий мониторинг
            </button>
            <button 
              @click="activeSection = 'complaints'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'complaints' }]"
            >
              <i class="fas fa-exclamation-triangle me-2"></i>
              Обращения граждан
            </button>
            <button 
              @click="activeSection = 'infrastructure'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'infrastructure' }]"
            >
              <i class="fas fa-building me-2"></i>
              Инфраструктура
            </button>
            <button 
              @click="activeSection = 'services'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'services' }]"
            >
              <i class="fas fa-concierge-bell me-2"></i>
              Услуги
            </button>
            <button 
              @click="activeSection = 'analytics'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'analytics' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Аналитика
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Общий мониторинг -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Общий мониторинг системы
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика обращений (30 дней)</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="complaintsChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Распределение по типам проблем</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="type in problemTypes" :key="type.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ type.name }}</span>
                        <span class="badge bg-secondary">{{ type.count }}</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :class="type.color"
                          :style="`width: ${(type.count / stats.totalComplaints) * 100}%`"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="row mt-3">
              <div class="col-md-12">
                <div class="card">
                  <div class="card-header">
                    <h6>Последние события</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="event in recentEvents" :key="event.id" class="d-flex align-items-center mb-2">
                      <i :class="getEventIcon(event.type)" class="me-3"></i>
                      <div class="flex-grow-1">
                        <div class="d-flex justify-content-between">
                          <span>{{ event.message }}</span>
                          <small class="text-muted">{{ formatTime(event.timestamp) }}</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Обращения граждан -->
        <div v-if="activeSection === 'complaints'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-exclamation-triangle"></i>
              Обращения граждан
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по адресу или номеру..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="complaintFilter = 'all'"
                  :class="['btn', complaintFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="complaintFilter = 'pending'"
                  :class="['btn', complaintFilter === 'pending' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Новые
                </button>
                <button 
                  @click="complaintFilter = 'in_progress'"
                  :class="['btn', complaintFilter === 'in_progress' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  В работе
                </button>
                <button 
                  @click="complaintFilter = 'resolved'"
                  :class="['btn', complaintFilter === 'resolved' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Решенные
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата</th>
                    <th>Адрес</th>
                    <th>Тип проблемы</th>
                    <th>Описание</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="complaint in filteredComplaints" :key="complaint.id" :class="getPriorityClass(complaint.priority)">
                    <td><strong>#{{ complaint.id }}</strong></td>
                    <td>
                      <small>{{ formatDate(complaint.created_at) }}</small>
                    </td>
                    <td>{{ complaint.address }}</td>
                    <td>
                      <span class="badge" :class="getProblemTypeBadgeClass(complaint.type)">
                        {{ getProblemTypeText(complaint.type) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ complaint.description.substring(0, 50) }}{{ complaint.description.length > 50 ? '...' : '' }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getStatusBadgeClass(complaint.status)]"
                      >
                        {{ getStatusText(complaint.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewComplaint(complaint.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="assignComplaint(complaint.id)"
                          v-if="complaint.status === 'pending'"
                          class="btn btn-outline-warning"
                          title="Назначить"
                        >
                          <i class="fas fa-user"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredComplaints.length === 0" class="text-center py-4">
              <i class="fas fa-exclamation-triangle fa-3x text-muted mb-3"></i>
              <p class="text-muted">Обращения не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Инфраструктура -->
        <div v-if="activeSection === 'infrastructure'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-building"></i>
              Состояние инфраструктуры
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="infrastructure in infrastructureObjects" :key="infrastructure.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i :class="getInfrastructureIcon(infrastructure.type)" class="me-2"></i>
                      {{ infrastructure.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ infrastructure.address }}</small>
                    </p>
                    <div class="mb-2">
                      <small class="text-muted">
                        Тип: {{ getInfrastructureTypeText(infrastructure.type) }}
                      </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <span 
                        :class="['badge', getInfrastructureStatusBadgeClass(infrastructure.status)]"
                      >
                        {{ getInfrastructureStatusText(infrastructure.status) }}
                      </span>
                      <small class="text-muted">
                        {{ infrastructure.lastInspection ? 'Обновлено: ' + formatDate(infrastructure.lastInspection) : 'Не осмотрено' }}
                      </small>
                    </div>
                  </div>
                  <div class="card-footer">
                    <button 
                      @click="inspectInfrastructure(infrastructure.id)"
                      class="btn btn-outline-primary btn-sm btn-block"
                    >
                      Осмотреть
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="infrastructureObjects.length === 0" class="text-center py-4">
              <i class="fas fa-building fa-3x text-muted mb-3"></i>
              <p class="text-muted">Объекты инфраструктуры не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Услуги -->
        <div v-if="activeSection === 'services'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-concierge-bell"></i>
              Жилищно-коммунальные услуги
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group btn-group-sm">
                <button 
                  @click="serviceFilter = 'all'"
                  :class="['btn', serviceFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все услуги
                </button>
                <button 
                  @click="serviceFilter = 'critical'"
                  :class="['btn', serviceFilter === 'critical' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Критические
                </button>
                <button 
                  @click="serviceFilter = 'normal'"
                  :class="['btn', serviceFilter === 'normal' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Обычные
                </button>
              </div>
              <button 
                @click="manageServices"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Добавить услугу
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Услуга</th>
                    <th>Поставщик</th>
                    <th>Зона покрытия</th>
                    <th>Статус</th>
                    <th>Последнее обновление</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="service in filteredServices" :key="service.id">
                    <td>
                      <strong>{{ service.name }}</strong>
                      <br>
                      <small class="text-muted">{{ service.description }}</small>
                    </td>
                    <td>{{ service.provider }}</td>
                    <td>{{ service.coverage_area }}</td>
                    <td>
                      <span 
                        :class="['badge', getServiceStatusBadgeClass(service.status)]"
                      >
                        {{ getServiceStatusText(service.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ formatDateTime(service.last_update) }}</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewService(service.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="updateService(service.id)"
                          class="btn btn-outline-warning"
                          title="Обновить"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredServices.length === 0" class="text-center py-4">
              <i class="fas fa-concierge-bell fa-3x text-muted mb-3"></i>
              <p class="text-muted">Услуги не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Аналитика -->
        <div v-if="activeSection === 'analytics'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Аналитика и отчеты
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6>Статистика по районам</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="district in districtStats" :key="district.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ district.name }}</span>
                        <span class="badge bg-info">{{ district.complaints }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика показателей</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Время ответа</span>
                        <span class="text-success">{{ analytics.responseTime }} ч</span>
                      </div>
                      <small class="text-muted">Среднее время обработки обращения</small>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Решено в срок</span>
                        <span class="text-success">{{ analytics.onTimeResolution }}%</span>
                      </div>
                      <small class="text-muted">Процент обращений, решенных в срок</small>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Повторные обращения</span>
                        <span class="text-warning">{{ analytics.repeatComplaints }}%</span>
                      </div>
                      <small class="text-muted">Процент повторных обращений</small>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6>Экспорт отчетов</h6>
                  </div>
                  <div class="card-body">
                    <button 
                      @click="exportReport('daily')"
                      class="btn btn-outline-primary btn-block mb-2"
                    >
                      <i class="fas fa-calendar-day me-2"></i>
                      Ежедневный отчет
                    </button>
                    <button 
                      @click="exportReport('weekly')"
                      class="btn btn-outline-primary btn-block mb-2"
                    >
                      <i class="fas fa-calendar-week me-2"></i>
                      Недельный отчет
                    </button>
                    <button 
                      @click="exportReport('monthly')"
                      class="btn btn-outline-primary btn-block mb-2"
                    >
                      <i class="fas fa-calendar-alt me-2"></i>
                      Месячный отчет
                    </button>
                  </div>
                </div>
              </div>
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
  name: 'CUKgh',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      searchQuery: '',
      complaintFilter: 'all',
      serviceFilter: 'all',
      
      // Ключевые показатели
      stats: {
        totalComplaints: 1247,
        resolvedToday: 23,
        pendingComplaints: 89,
        satisfaction: 87
      },

      // Обращения граждан
      complaints: [
        {
          id: 1001,
          created_at: new Date('2024-01-15T14:30:00'),
          address: 'г. Москва, ул. Тверская, д. 15',
          type: 'heating',
          description: 'Отсутствует отопление в квартире уже 3 дня',
          status: 'pending',
          priority: 'high'
        },
        {
          id: 1002,
          created_at: new Date('2024-01-15T13:15:00'),
          address: 'г. Москва, пр-т Мира, д. 42',
          type: 'water',
          description: 'Протечка воды в подвале',
          status: 'in_progress',
          priority: 'medium'
        },
        {
          id: 1003,
          created_at: new Date('2024-01-15T12:00:00'),
          address: 'г. Москва, ул. Ленина, д. 7',
          type: 'electricity',
          description: 'Перебои с электричеством',
          status: 'resolved',
          priority: 'low'
        }
      ],

      // Объекты инфраструктуры
      infrastructureObjects: [
        {
          id: 1,
          name: 'Котельная №1 "Северная"',
          type: 'boiler',
          address: 'г. Москва, ул. Северная, д. 1',
          status: 'operational',
          lastInspection: new Date('2024-01-10')
        },
        {
          id: 2,
          name: 'Очистные сооружения "Западные"',
          type: 'treatment',
          address: 'г. Москва, ул. Очистная, д. 25',
          status: 'maintenance',
          lastInspection: new Date('2024-01-08')
        },
        {
          id: 3,
          name: 'Электроподстанция "Центральная"',
          type: 'power',
          address: 'г. Москва, ул. Электрическая, д. 10',
          status: 'operational',
          lastInspection: new Date('2024-01-12')
        }
      ],

      // Услуги
      services: [
        {
          id: 1,
          name: 'Холодное водоснабжение',
          description: 'Подача холодной воды',
          provider: 'Мосводоканал',
          coverage_area: 'Весь город',
          status: 'operational',
          last_update: new Date('2024-01-15T10:00:00')
        },
        {
          id: 2,
          name: 'Отопление',
          description: 'Центральное отопление',
          provider: 'Мосэнерго',
          coverage_area: 'Центральный и Северный районы',
          status: 'operational',
          last_update: new Date('2024-01-15T11:30:00')
        },
        {
          id: 3,
          name: 'Газоснабжение',
          description: 'Подача природного газа',
          provider: 'Мосгаз',
          coverage_area: 'Весь город',
          status: 'operational',
          last_update: new Date('2024-01-15T09:45:00')
        }
      ],

      // Типы проблем
      problemTypes: [
        { name: 'Отопление', count: 125, color: 'bg-warning' },
        { name: 'Водоснабжение', count: 89, color: 'bg-primary' },
        { name: 'Электроснабжение', count: 67, color: 'bg-success' },
        { name: 'Газоснабжение', count: 45, color: 'bg-danger' },
        { name: 'Прочие', count: 23, color: 'bg-secondary' }
      ],

      // Последние события
      recentEvents: [
        {
          id: 1,
          type: 'complaint_received',
          message: 'Новое обращение #1001 по отоплению',
          timestamp: new Date('2024-01-15T14:30:00')
        },
        {
          id: 2,
          type: 'complaint_resolved',
          message: 'Обращение #1003 успешно решено',
          timestamp: new Date('2024-01-15T12:15:00')
        },
        {
          id: 3,
          type: 'service_update',
          message: 'Обновлен статус водоснабжения',
          timestamp: new Date('2024-01-15T11:45:00')
        }
      ],

      // Статистика по районам
      districtStats: [
        { name: 'Центральный', complaints: 156 },
        { name: 'Северный', complaints: 134 },
        { name: 'Южный', complaints: 98 },
        { name: 'Восточный', complaints: 87 },
        { name: 'Западный', complaints: 76 }
      ],

      // Аналитические данные
      analytics: {
        responseTime: 4.2,
        onTimeResolution: 89,
        repeatComplaints: 7
      }
    };
  },
  computed: {
    filteredComplaints() {
      let filtered = this.complaints;
      
      if (this.searchQuery) {
        filtered = filtered.filter(complaint => 
          complaint.address.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          complaint.id.toString().includes(this.searchQuery)
        );
      }
      
      if (this.complaintFilter !== 'all') {
        filtered = filtered.filter(complaint => complaint.status === this.complaintFilter);
      }
      
      return filtered;
    },

    filteredServices() {
      let filtered = this.services;
      
      if (this.serviceFilter === 'critical') {
        filtered = filtered.filter(service => 
          service.status === 'disrupted' || service.status === 'maintenance'
        );
      } else if (this.serviceFilter === 'normal') {
        filtered = filtered.filter(service => service.status === 'operational');
      }
      
      return filtered;
    }
  },
  methods: {
    async refreshData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Имитация обновления данных
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('Данные ЦУ КГХ обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    generateReport() {
      console.log('Генерация отчета ЦУ КГХ');
      alert('Генерация отчета ЦУ КГХ (заглушка)');
    },

    viewComplaint(complaintId) {
      console.log(`Просмотр обращения ${complaintId}`);
      alert(`Просмотр обращения ${complaintId} (заглушка)`);
    },

    assignComplaint(complaintId) {
      console.log(`Назначение обращения ${complaintId}`);
      alert(`Назначение обращения ${complaintId} (заглушка)`);
    },

    inspectInfrastructure(infrastructureId) {
      console.log(`Осмотр инфраструктуры ${infrastructureId}`);
      alert(`Осмотр инфраструктуры ${infrastructureId} (заглушка)`);
    },

    viewService(serviceId) {
      console.log(`Просмотр услуги ${serviceId}`);
      alert(`Просмотр услуги ${serviceId} (заглушка)`);
    },

    updateService(serviceId) {
      console.log(`Обновление услуги ${serviceId}`);
      alert(`Обновление услуги ${serviceId} (заглушка)`);
    },

    manageServices() {
      console.log('Управление услугами');
      alert('Управление услугами (заглушка)');
    },

    exportReport(reportType) {
      console.log(`Экспорт ${reportType} отчета`);
      alert(`Экспорт ${reportType} отчета (заглушка)`);
    },

    // Вспомогательные методы
    getPriorityClass(priority) {
      return priority === 'high' ? 'table-danger' : priority === 'medium' ? 'table-warning' : '';
    },

    getProblemTypeBadgeClass(type) {
      const classes = {
        heating: 'bg-warning',
        water: 'bg-primary',
        electricity: 'bg-success',
        gas: 'bg-danger'
      };
      return classes[type] || 'bg-secondary';
    },

    getProblemTypeText(type) {
      const texts = {
        heating: 'Отопление',
        water: 'Водоснабжение',
        electricity: 'Электроснабжение',
        gas: 'Газоснабжение'
      };
      return texts[type] || type;
    },

    getStatusBadgeClass(status) {
      const classes = {
        pending: 'bg-warning',
        in_progress: 'bg-primary',
        resolved: 'bg-success'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusText(status) {
      const texts = {
        pending: 'Новое',
        in_progress: 'В работе',
        resolved: 'Решено'
      };
      return texts[status] || status;
    },

    getInfrastructureIcon(type) {
      const icons = {
        boiler: 'fas fa-fire text-danger',
        treatment: 'fas fa-tint text-primary',
        power: 'fas fa-bolt text-warning'
      };
      return icons[type] || 'fas fa-building text-secondary';
    },

    getInfrastructureTypeText(type) {
      const texts = {
        boiler: 'Котельная',
        treatment: 'Очистные сооружения',
        power: 'Электроподстанция'
      };
      return texts[type] || type;
    },

    getInfrastructureStatusBadgeClass(status) {
      const classes = {
        operational: 'bg-success',
        maintenance: 'bg-warning',
        disconnected: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getInfrastructureStatusText(status) {
      const texts = {
        operational: 'В работе',
        maintenance: 'На обслуживании',
        disconnected: 'Отключена'
      };
      return texts[status] || status;
    },

    getServiceStatusBadgeClass(status) {
      const classes = {
        operational: 'bg-success',
        maintenance: 'bg-warning',
        disrupted: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getServiceStatusText(status) {
      const texts = {
        operational: 'В работе',
        maintenance: 'На обслуживании',
        disrupted: 'Нарушена'
      };
      return texts[status] || status;
    },

    getEventIcon(type) {
      const icons = {
        complaint_received: 'fas fa-exclamation-triangle text-warning',
        complaint_resolved: 'fas fa-check-circle text-success',
        service_update: 'fas fa-wrench text-primary'
      };
      return icons[type] || 'fas fa-info-circle text-secondary';
    },

    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleDateString('ru-RU');
    },

    formatDateTime(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleString('ru-RU');
    },

    formatTime(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleTimeString('ru-RU', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    }
  },
  mounted() {
    console.log('Компонента ЦУ КГХ инициализирована');
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

.table-danger {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

.table-warning {
  background-color: rgba(255, 193, 7, 0.1) !important;
}

.bg-primary {
  background-color: #007bff !important;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.bg-info {
  background-color: #17a2b8 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}

.progress {
  background-color: #e9ecef;
}

.progress-bar {
  background-color: #007bff;
}

.btn-block {
  width: 100%;
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
  
  .input-group {
    margin-bottom: 10px;
  }
}
</style>