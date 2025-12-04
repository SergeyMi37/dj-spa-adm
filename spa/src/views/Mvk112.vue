<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-phone"></i> Служба 112</h2>
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
              @click="newEmergencyCall" 
              class="btn btn-danger btn-sm"
            >
              <i class="fas fa-plus"></i>
              Новый вызов
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Статус панель -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 text-center">
                <h3 class="text-danger">{{ stats.activeCalls }}</h3>
                <small class="text-muted">Активных вызовов</small>
              </div>
              <div class="col-md-3 text-center">
                <h3 class="text-warning">{{ stats.pendingCalls }}</h3>
                <small class="text-muted">Ожидающих ответа</small>
              </div>
              <div class="col-md-3 text-center">
                <h3 class="text-success">{{ stats.completedToday }}</h3>
                <small class="text-muted">Обработано сегодня</small>
              </div>
              <div class="col-md-3 text-center">
                <h3 class="text-info">{{ stats.averageResponseTime }}</h3>
                <small class="text-muted">Среднее время ответа (мин)</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации -->
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
              @click="activeSection = 'active'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'active' }]"
            >
              <i class="fas fa-phone me-2"></i>
              Активные вызовы
            </button>
            <button 
              @click="activeSection = 'history'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'history' }]"
            >
              <i class="fas fa-history me-2"></i>
              История вызовов
            </button>
            <button 
              @click="activeSection = 'summary'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'summary' }]"
            >
              <i class="fas fa-chart-line me-2"></i>
              Оперативная сводка
            </button>
            <button 
              @click="activeSection = 'statistics'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'statistics' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Статистика
            </button>
            <button 
              @click="activeSection = 'personnel'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'personnel' }]"
            >
              <i class="fas fa-users me-2"></i>
              Персонал
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Активные вызовы -->
        <div v-if="activeSection === 'active'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-phone"></i>
              Активные вызовы
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по номеру или адресу..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="callFilter = 'all'"
                  :class="['btn', callFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="callFilter = 'emergency'"
                  :class="['btn', callFilter === 'emergency' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Экстренные
                </button>
                <button 
                  @click="callFilter = 'urgent'"
                  :class="['btn', callFilter === 'urgent' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Срочные
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Время</th>
                    <th>Тип</th>
                    <th>Адрес</th>
                    <th>Описание</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="call in filteredActiveCalls" :key="call.id" :class="getCallPriorityClass(call.priority)">
                    <td><strong>#{{ call.id }}</strong></td>
                    <td>
                      <small>{{ formatTime(call.created_at) }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getPriorityBadgeClass(call.priority)">
                        {{ getPriorityText(call.priority) }}
                      </span>
                    </td>
                    <td>{{ call.address }}</td>
                    <td>
                      <small>{{ call.description.substring(0, 50) }}{{ call.description.length > 50 ? '...' : '' }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getStatusBadgeClass(call.status)">
                        {{ getStatusText(call.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="takeCall(call.id)"
                          v-if="call.status === 'new'"
                          class="btn btn-outline-success"
                          title="Взять вызов"
                        >
                          <i class="fas fa-phone"></i>
                        </button>
                        <button 
                          @click="viewCall(call.id)"
                          class="btn btn-outline-primary"
                          title="Подробнее"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="assignCall(call.id)"
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

            <div v-if="filteredActiveCalls.length === 0" class="text-center py-4">
              <i class="fas fa-phone fa-3x text-muted mb-3"></i>
              <p class="text-muted">Активные вызовы не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел История вызовов -->
        <div v-if="activeSection === 'history'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-history"></i>
              История вызовов
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div>
                <input 
                  v-model="dateFilter"
                  type="date" 
                  class="form-control form-control-sm" 
                  style="width: 150px; display: inline-block;"
                >
                <select v-model="statusFilter" class="form-control form-control-sm" style="width: 150px; display: inline-block; margin-left: 10px;">
                  <option value="all">Все статусы</option>
                  <option value="completed">Завершенные</option>
                  <option value="cancelled">Отмененные</option>
                  <option value="transferred">Переведенные</option>
                </select>
              </div>
              <button 
                @click="exportHistory"
                class="btn btn-outline-success btn-sm"
              >
                <i class="fas fa-download"></i>
                Экспорт
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата/Время</th>
                    <th>Тип</th>
                    <th>Адрес</th>
                    <th>Оперативные службы</th>
                    <th>Статус</th>
                    <th>Время обработки</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="call in filteredHistoryCalls" :key="call.id">
                    <td><strong>#{{ call.id }}</strong></td>
                    <td>
                      <small>{{ formatDateTime(call.created_at) }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getPriorityBadgeClass(call.priority)">
                        {{ getPriorityText(call.priority) }}
                      </span>
                    </td>
                    <td>{{ call.address }}</td>
                    <td>
                      <span v-for="service in call.services" :key="service" class="badge bg-info me-1">
                        {{ service }}
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatusBadgeClass(call.status)">
                        {{ getStatusText(call.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ call.processing_time }} мин</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewCallHistory(call.id)"
                          class="btn btn-outline-primary"
                          title="Подробнее"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="reopenCall(call.id)"
                          class="btn btn-outline-warning"
                          title="Возобновить"
                        >
                          <i class="fas fa-redo"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredHistoryCalls.length === 0" class="text-center py-4">
              <i class="fas fa-history fa-3x text-muted mb-3"></i>
              <p class="text-muted">История вызовов пуста</p>
            </div>
          </div>
        </div>

        <!-- Раздел Оперативная сводка -->
        <div v-if="activeSection === 'summary'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Оперативная сводка
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <div class="card bg-light">
                  <div class="card-body">
                    <h6>Статистика по времени</h6>
                    <div class="row text-center">
                      <div class="col-4">
                        <h4 class="text-primary">{{ summary.hourlyCalls }}</h4>
                        <small>за час</small>
                      </div>
                      <div class="col-4">
                        <h4 class="text-warning">{{ summary.dailyCalls }}</h4>
                        <small>за день</small>
                      </div>
                      <div class="col-4">
                        <h4 class="text-success">{{ summary.weeklyCalls }}</h4>
                        <small>за неделю</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <div class="card bg-light">
                  <div class="card-body">
                    <h6>Распределение по типам</h6>
                    <div v-for="type in summary.callTypes" :key="type.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ type.name }}</span>
                        <span class="badge bg-primary">{{ type.count }}</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :style="`width: ${(type.count / summary.totalCalls) * 100}%`"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="row">
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

        <!-- Раздел Статистика -->
        <div v-if="activeSection === 'statistics'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Статистика
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика вызовов (7 дней)</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="callsChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Распределение по районам</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="district in districtStats" :key="district.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ district.name }}</span>
                        <span class="badge bg-secondary">{{ district.count }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Персонал -->
        <div v-if="activeSection === 'personnel'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-users"></i>
              Персонал
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group btn-group-sm">
                <button 
                  @click="personnelFilter = 'all'"
                  :class="['btn', personnelFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="personnelFilter = 'online'"
                  :class="['btn', personnelFilter === 'online' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  На линии
                </button>
                <button 
                  @click="personnelFilter = 'offline'"
                  :class="['btn', personnelFilter === 'offline' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Не на линии
                </button>
              </div>
              <button 
                @click="addOperator"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-user-plus"></i>
                Добавить оператора
              </button>
            </div>

            <div class="row">
              <div class="col-md-4 mb-3" v-for="operator in filteredOperators" :key="operator.id">
                <div class="card h-100">
                  <div class="card-body">
                    <div class="d-flex align-items-center mb-2">
                      <div 
                        :class="['rounded-circle', 'me-3', operator.isOnline ? 'bg-success' : 'bg-secondary']" 
                        style="width: 12px; height: 12px;"
                      ></div>
                      <h6 class="mb-0">{{ operator.name }}</h6>
                    </div>
                    <p class="card-text">
                      <small class="text-muted">
                        <i class="fas fa-phone me-1"></i>
                        {{ operator.phone }}
                      </small>
                    </p>
                    <div class="row text-center">
                      <div class="col-6">
                        <strong>{{ operator.callsHandled }}</strong>
                        <br>
                        <small class="text-muted">Обработано</small>
                      </div>
                      <div class="col-6">
                        <strong>{{ operator.averageTime }}м</strong>
                        <br>
                        <small class="text-muted">Среднее время</small>
                      </div>
                    </div>
                    <div class="mt-2">
                      <button 
                        @click="viewOperator(operator.id)"
                        class="btn btn-outline-primary btn-sm btn-block"
                      >
                        Подробнее
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="filteredOperators.length === 0" class="text-center py-4">
              <i class="fas fa-users fa-3x text-muted mb-3"></i>
              <p class="text-muted">Операторы не найдены</p>
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
  name: 'Mvk112',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'active',
      searchQuery: '',
      callFilter: 'all',
      dateFilter: '',
      statusFilter: 'all',
      personnelFilter: 'all',
      
      // Статистика
      stats: {
        activeCalls: 15,
        pendingCalls: 3,
        completedToday: 127,
        averageResponseTime: 2.3
      },

      // Активные вызовы
      activeCalls: [
        {
          id: 1001,
          created_at: new Date('2024-01-15T14:30:00'),
          priority: 'emergency',
          address: 'г. Москва, ул. Тверская, д. 15',
          description: 'Пожар в квартире на 5 этаже, требуется срочная эвакуация',
          status: 'in_progress',
          assigned_to: 'Оператор 1'
        },
        {
          id: 1002,
          created_at: new Date('2024-01-15T14:25:00'),
          priority: 'urgent',
          address: 'г. Москва, пр-т Мира, д. 42',
          description: 'ДТП с пострадавшими, требуется медицинская помощь',
          status: 'new',
          assigned_to: null
        },
        {
          id: 1003,
          created_at: new Date('2024-01-15T14:20:00'),
          priority: 'urgent',
          address: 'г. Москва, ул. Ленина, д. 7',
          description: 'Протечка воды в подвале, затопление',
          status: 'assigned',
          assigned_to: 'Оператор 2'
        }
      ],

      // История вызовов
      historyCalls: [
        {
          id: 1000,
          created_at: new Date('2024-01-15T13:45:00'),
          priority: 'emergency',
          address: 'г. Москва, ул. Горького, д. 10',
          description: 'Взрыв газа в жилом доме',
          status: 'completed',
          services: ['МЧС', 'Скорая помощь', 'Полиция'],
          processing_time: 25
        },
        {
          id: 999,
          created_at: new Date('2024-01-15T13:30:00'),
          priority: 'urgent',
          address: 'г. Москва, ул. Пушкина, д. 5',
          description: 'Несчастный случай на производстве',
          status: 'completed',
          services: ['Скорая помощь'],
          processing_time: 15
        }
      ],

      // Оперативная сводка
      summary: {
        hourlyCalls: 8,
        dailyCalls: 127,
        weeklyCalls: 856,
        totalCalls: 127,
        callTypes: [
          { name: 'Пожары', count: 12 },
          { name: 'ДТП', count: 23 },
          { name: 'Медицинские', count: 45 },
          { name: 'Происшествия', count: 18 },
          { name: 'Другие', count: 29 }
        ]
      },

      // Последние события
      recentEvents: [
        {
          id: 1,
          type: 'new_call',
          message: 'Новый экстренный вызов №1001',
          timestamp: new Date('2024-01-15T14:30:00')
        },
        {
          id: 2,
          type: 'assignment',
          message: 'Вызов №1002 назначен оператору',
          timestamp: new Date('2024-01-15T14:28:00')
        },
        {
          id: 3,
          type: 'completion',
          message: 'Вызов №1000 успешно завершен',
          timestamp: new Date('2024-01-15T14:25:00')
        }
      ],

      // Статистика по районам
      districtStats: [
        { name: 'Центральный', count: 35 },
        { name: 'Северный', count: 28 },
        { name: 'Южный', count: 22 },
        { name: 'Восточный', count: 19 },
        { name: 'Западный', count: 23 }
      ],

      // Персонал
      operators: [
        {
          id: 1,
          name: 'Иванов И.И.',
          phone: '+7 (495) 123-45-67',
          isOnline: true,
          callsHandled: 45,
          averageTime: 3.2
        },
        {
          id: 2,
          name: 'Петров П.П.',
          phone: '+7 (495) 234-56-78',
          isOnline: true,
          callsHandled: 38,
          averageTime: 2.8
        },
        {
          id: 3,
          name: 'Сидоров С.С.',
          phone: '+7 (495) 345-67-89',
          isOnline: false,
          callsHandled: 52,
          averageTime: 4.1
        }
      ]
    };
  },
  computed: {
    filteredActiveCalls() {
      let filtered = this.activeCalls;
      
      if (this.searchQuery) {
        filtered = filtered.filter(call => 
          call.address.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          call.id.toString().includes(this.searchQuery)
        );
      }
      
      if (this.callFilter !== 'all') {
        filtered = filtered.filter(call => call.priority === this.callFilter);
      }
      
      return filtered;
    },

    filteredHistoryCalls() {
      let filtered = this.historyCalls;
      
      if (this.statusFilter !== 'all') {
        filtered = filtered.filter(call => call.status === this.statusFilter);
      }
      
      return filtered;
    },

    filteredOperators() {
      let filtered = this.operators;
      
      if (this.personnelFilter !== 'all') {
        filtered = filtered.filter(operator => 
          this.personnelFilter === 'online' ? operator.isOnline : !operator.isOnline
        );
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
        console.log('Данные службы 112 обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    newEmergencyCall() {
      console.log('Создание нового экстренного вызова');
      alert('Создание нового экстренного вызова (заглушка)');
    },

    takeCall(callId) {
      const call = this.activeCalls.find(c => c.id === callId);
      if (call) {
        call.status = 'in_progress';
        call.assigned_to = 'Текущий оператор';
      }
      console.log(`Вызов ${callId} взят в работу`);
    },

    viewCall(callId) {
      console.log(`Просмотр вызова ${callId}`);
      alert(`Просмотр вызова ${callId} (заглушка)`);
    },

    assignCall(callId) {
      console.log(`Назначение вызова ${callId}`);
      alert(`Назначение вызова ${callId} (заглушка)`);
    },

    viewCallHistory(callId) {
      console.log(`Просмотр истории вызова ${callId}`);
      alert(`Просмотр истории вызова ${callId} (заглушка)`);
    },

    reopenCall(callId) {
      console.log(`Возобновление вызова ${callId}`);
      alert(`Возобновление вызова ${callId} (заглушка)`);
    },

    exportHistory() {
      console.log('Экспорт истории вызовов');
      alert('Экспорт истории вызовов (заглушка)');
    },

    addOperator() {
      console.log('Добавление нового оператора');
      alert('Добавление нового оператора (заглушка)');
    },

    viewOperator(operatorId) {
      console.log(`Просмотр оператора ${operatorId}`);
      alert(`Просмотр оператора ${operatorId} (заглушка)`);
    },

    // Вспомогательные методы
    getPriorityBadgeClass(priority) {
      const classes = {
        emergency: 'bg-danger',
        urgent: 'bg-warning',
        normal: 'bg-info'
      };
      return classes[priority] || 'bg-secondary';
    },

    getPriorityText(priority) {
      const texts = {
        emergency: 'Экстренный',
        urgent: 'Срочный',
        normal: 'Обычный'
      };
      return texts[priority] || priority;
    },

    getStatusBadgeClass(status) {
      const classes = {
        new: 'bg-secondary',
        in_progress: 'bg-primary',
        assigned: 'bg-warning',
        completed: 'bg-success',
        cancelled: 'bg-danger',
        transferred: 'bg-info'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusText(status) {
      const texts = {
        new: 'Новый',
        in_progress: 'В обработке',
        assigned: 'Назначен',
        completed: 'Завершен',
        cancelled: 'Отменен',
        transferred: 'Переведен'
      };
      return texts[status] || status;
    },

    getCallPriorityClass(priority) {
      return priority === 'emergency' ? 'table-danger' : '';
    },

    getEventIcon(type) {
      const icons = {
        new_call: 'fas fa-phone text-danger',
        assignment: 'fas fa-user-plus text-primary',
        completion: 'fas fa-check-circle text-success'
      };
      return icons[type] || 'fas fa-info-circle text-secondary';
    },

    formatTime(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleTimeString('ru-RU', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    },

    formatDateTime(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
  mounted() {
    console.log('Компонента службы 112 инициализирована');
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
  background-color: #dc3545;
  border-color: #dc3545;
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

.bg-light {
  background-color: #f8f9fa !important;
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