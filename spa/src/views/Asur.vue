<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-file-alt"></i> АСУР СМЭВ</h2>
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
              @click="newRequest" 
              class="btn btn-success btn-sm"
            >
              <i class="fas fa-plus"></i>
              Новый запрос
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
              Автоматизированная система управления регионом СМЭВ
            </h5>
            <p class="card-text">
              СМЭВ (Система межведомственного электронного взаимодействия) обеспечивает 
              межведомственный обмен электронными документами между федеральными, региональными 
              и муниципальными органами власти для предоставления государственных услуг.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации АСУР СМЭВ -->
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
              @click="activeSection = 'requests'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'requests' }]"
            >
              <i class="fas fa-paper-plane me-2"></i>
              Запросы
            </button>
            <button 
              @click="activeSection = 'responses'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'responses' }]"
            >
              <i class="fas fa-inbox me-2"></i>
              Ответы
            </button>
            <button 
              @click="activeSection = 'services'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'services' }]"
            >
              <i class="fas fa-concierge-bell me-2"></i>
              Услуги
            </button>
            <button 
              @click="activeSection = 'departments'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'departments' }]"
            >
              <i class="fas fa-building me-2"></i>
              Органы власти
            </button>
            <button 
              @click="activeSection = 'monitoring'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'monitoring' }]"
            >
              <i class="fas fa-chart-line me-2"></i>
              Мониторинг
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Запросы -->
        <div v-if="activeSection === 'requests'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-paper-plane"></i>
              Межведомственные запросы
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по номеру или услуге..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="requestFilter = 'all'"
                  :class="['btn', requestFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="requestFilter = 'pending'"
                  :class="['btn', requestFilter === 'pending' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Ожидающие
                </button>
                <button 
                  @click="requestFilter = 'completed'"
                  :class="['btn', requestFilter === 'completed' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Обработанные
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>ID запроса</th>
                    <th>Услуга</th>
                    <th>Орган власти</th>
                    <th>Дата отправки</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in filteredRequests" :key="request.id">
                    <td><strong>#{{ request.id }}</strong></td>
                    <td>{{ request.service_name }}</td>
                    <td>
                      <small>{{ request.department }}</small>
                    </td>
                    <td>
                      <small>{{ formatDate(request.created_at) }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getStatusBadgeClass(request.status)]"
                      >
                        {{ getStatusText(request.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewRequest(request.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="resendRequest(request.id)"
                          v-if="request.status === 'error'"
                          class="btn btn-outline-warning"
                          title="Повторить отправку"
                        >
                          <i class="fas fa-redo"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredRequests.length === 0" class="text-center py-4">
              <i class="fas fa-paper-plane fa-3x text-muted mb-3"></i>
              <p class="text-muted">Запросы не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Ответы -->
        <div v-if="activeSection === 'responses'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-inbox"></i>
              Полученные ответы
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div>
                <select v-model="responseFilter" class="form-control form-control-sm" style="width: 150px; display: inline-block;">
                  <option value="all">Все ответы</option>
                  <option value="success">Успешные</option>
                  <option value="error">Ошибочные</option>
                  <option value="pending">В обработке</option>
                </select>
              </div>
              <button 
                @click="exportResponses"
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
                    <th>ID ответа</th>
                    <th>ID запроса</th>
                    <th>Услуга</th>
                    <th>Дата получения</th>
                    <th>Статус</th>
                    <th>Время обработки</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="response in filteredResponses" :key="response.id">
                    <td><strong>#{{ response.id }}</strong></td>
                    <td>
                      <a href="#" @click.prevent="viewRequest(response.request_id)" class="text-decoration-none">
                        #{{ response.request_id }}
                      </a>
                    </td>
                    <td>{{ response.service_name }}</td>
                    <td>
                      <small>{{ formatDateTime(response.received_at) }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getResponseStatusBadgeClass(response.status)]"
                      >
                        {{ getResponseStatusText(response.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ response.processing_time }} сек</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewResponse(response.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="downloadResponse(response.id)"
                          class="btn btn-outline-success"
                          title="Скачать"
                        >
                          <i class="fas fa-download"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredResponses.length === 0" class="text-center py-4">
              <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
              <p class="text-muted">Ответы не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Услуги -->
        <div v-if="activeSection === 'services'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-concierge-bell"></i>
              Государственные услуги
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="service in services" :key="service.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i :class="getServiceIcon(service.category)" class="me-2"></i>
                      {{ service.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ service.description }}</small>
                    </p>
                    <div class="mb-2">
                      <small class="text-muted">
                        <i class="fas fa-building me-1"></i>
                        {{ service.department }}
                      </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <span 
                        :class="['badge', service.status === 'active' ? 'bg-success' : 'bg-danger']"
                      >
                        {{ service.status === 'active' ? 'Активная' : 'Неактивная' }}
                      </span>
                      <small class="text-muted">{{ service.requests_count }} запросов</small>
                    </div>
                    <div class="mt-2">
                      <button 
                        @click="viewService(service.id)"
                        class="btn btn-outline-primary btn-sm btn-block"
                      >
                        Подробнее
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="services.length === 0" class="text-center py-4">
              <i class="fas fa-concierge-bell fa-3x text-muted mb-3"></i>
              <p class="text-muted">Услуги не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Органы власти -->
        <div v-if="activeSection === 'departments'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-building"></i>
              Органы власти
            </h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Регион</th>
                    <th>Статус подключения</th>
                    <th>Количество услуг</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="dept in departments" :key="dept.id">
                    <td>
                      <strong>{{ dept.name }}</strong>
                      <br>
                      <small class="text-muted">{{ dept.short_name }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getDepartmentTypeBadgeClass(dept.type)">
                        {{ getDepartmentTypeText(dept.type) }}
                      </span>
                    </td>
                    <td>{{ dept.region }}</td>
                    <td>
                      <span 
                        :class="['badge', dept.connection_status === 'connected' ? 'bg-success' : 'bg-danger']"
                      >
                        {{ dept.connection_status === 'connected' ? 'Подключен' : 'Отключен' }}
                      </span>
                    </td>
                    <td>{{ dept.services_count }}</td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewDepartment(dept.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="testConnection(dept.id)"
                          class="btn btn-outline-warning"
                          title="Проверить связь"
                        >
                          <i class="fas fa-plug"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="departments.length === 0" class="text-center py-4">
              <i class="fas fa-building fa-3x text-muted mb-3"></i>
              <p class="text-muted">Органы власти не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Мониторинг -->
        <div v-if="activeSection === 'monitoring'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Мониторинг системы
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 mb-3">
                <div class="card bg-primary text-white">
                  <div class="card-body text-center">
                    <h3>{{ stats.totalRequests }}</h3>
                    <p class="mb-0">Всего запросов</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-success text-white">
                  <div class="card-body text-center">
                    <h3>{{ stats.successfulRequests }}</h3>
                    <p class="mb-0">Успешных</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-warning text-white">
                  <div class="card-body text-center">
                    <h3>{{ stats.pendingRequests }}</h3>
                    <p class="mb-0">В обработке</p>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-danger text-white">
                  <div class="card-body text-center">
                    <h3>{{ stats.errorRequests }}</h3>
                    <p class="mb-0">Ошибок</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Производительность за последние 7 дней</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="performanceChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Распределение по типам услуг</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="type in serviceTypeStats" :key="type.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ type.name }}</span>
                        <span class="badge bg-secondary">{{ type.count }}</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :style="`width: ${(type.count / stats.totalRequests) * 100}%`"
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
  name: 'Asur',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'requests',
      searchQuery: '',
      requestFilter: 'all',
      responseFilter: 'all',
      
      // Статистика
      stats: {
        totalRequests: 1247,
        successfulRequests: 1189,
        pendingRequests: 12,
        errorRequests: 46
      },

      // Запросы
      requests: [
        {
          id: 1001,
          service_name: 'Проверка штрафов ГИБДД',
          department: 'ГИБДД ГУ МВД России',
          created_at: new Date('2024-01-15T10:30:00'),
          status: 'pending'
        },
        {
          id: 1002,
          service_name: 'Получение справки о составе семьи',
          department: 'ФМС России',
          created_at: new Date('2024-01-15T09:15:00'),
          status: 'completed'
        },
        {
          id: 1003,
          service_name: 'Проверка налоговых задолженностей',
          department: 'ФНС России',
          created_at: new Date('2024-01-15T08:45:00'),
          status: 'error'
        }
      ],

      // Ответы
      responses: [
        {
          id: 2001,
          request_id: 1002,
          service_name: 'Получение справки о составе семьи',
          received_at: new Date('2024-01-15T09:20:00'),
          status: 'success',
          processing_time: 5
        },
        {
          id: 2002,
          request_id: 1001,
          service_name: 'Проверка штрафов ГИБДД',
          received_at: new Date('2024-01-15T10:35:00'),
          status: 'pending',
          processing_time: 0
        }
      ],

      // Услуги
      services: [
        {
          id: 1,
          name: 'Проверка штрафов ГИБДД',
          description: 'Проверка наличия неоплаченных штрафов за нарушения ПДД',
          department: 'ГИБДД ГУ МВД России',
          category: 'traffic',
          status: 'active',
          requests_count: 345
        },
        {
          id: 2,
          name: 'Справка о составе семьи',
          description: 'Получение справки о составе семьи из ЗАГС',
          department: 'ЗАГС России',
          category: 'civil',
          status: 'active',
          requests_count: 234
        },
        {
          id: 3,
          name: 'Налоговые задолженности',
          description: 'Проверка задолженности по налогам и сборам',
          department: 'ФНС России',
          category: 'tax',
          status: 'active',
          requests_count: 567
        },
        {
          id: 4,
          name: 'Справка о доходах',
          description: 'Получение справки о доходах физического лица',
          department: 'ФНС России',
          category: 'tax',
          status: 'inactive',
          requests_count: 101
        }
      ],

      // Органы власти
      departments: [
        {
          id: 1,
          name: 'Главное управление МВД России по г. Москве',
          short_name: 'ГУ МВД России по г. Москве',
          type: 'federal',
          region: 'Москва',
          connection_status: 'connected',
          services_count: 8
        },
        {
          id: 2,
          name: 'Федеральная налоговая служба',
          short_name: 'ФНС России',
          type: 'federal',
          region: 'Москва',
          connection_status: 'connected',
          services_count: 12
        },
        {
          id: 3,
          name: 'Управление ЗАГС Москвы',
          short_name: 'ЗАГС Москвы',
          type: 'regional',
          region: 'Москва',
          connection_status: 'connected',
          services_count: 5
        },
        {
          id: 4,
          name: 'Департамент социального развития',
          short_name: 'ДСР Москвы',
          type: 'regional',
          region: 'Москва',
          connection_status: 'disconnected',
          services_count: 3
        }
      ],

      // Статистика по типам услуг
      serviceTypeStats: [
        { name: 'Налоговые', count: 567 },
        { name: 'Гражданские', count: 345 },
        { name: 'Социальные', count: 234 },
        { name: 'Градостроительные', count: 101 }
      ],

      // Последние события
      recentEvents: [
        {
          id: 1,
          type: 'request_sent',
          message: 'Запрос #1001 успешно отправлен в ГИБДД',
          timestamp: new Date('2024-01-15T10:30:00')
        },
        {
          id: 2,
          type: 'response_received',
          message: 'Получен ответ на запрос #1002 от ФМС',
          timestamp: new Date('2024-01-15T09:20:00')
        },
        {
          id: 3,
          type: 'error',
          message: 'Ошибка при отправке запроса #1003 в ФНС',
          timestamp: new Date('2024-01-15T08:45:00')
        }
      ]
    };
  },
  computed: {
    filteredRequests() {
      let filtered = this.requests;
      
      if (this.searchQuery) {
        filtered = filtered.filter(request => 
          request.service_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          request.id.toString().includes(this.searchQuery)
        );
      }
      
      if (this.requestFilter !== 'all') {
        filtered = filtered.filter(request => request.status === this.requestFilter);
      }
      
      return filtered;
    },

    filteredResponses() {
      let filtered = this.responses;
      
      if (this.responseFilter !== 'all') {
        filtered = filtered.filter(response => response.status === this.responseFilter);
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
        console.log('Данные АСУР СМЭВ обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    newRequest() {
      console.log('Создание нового межведомственного запроса');
      alert('Создание нового межведомственного запроса (заглушка)');
    },

    viewRequest(requestId) {
      console.log(`Просмотр запроса ${requestId}`);
      alert(`Просмотр запроса ${requestId} (заглушка)`);
    },

    resendRequest(requestId) {
      console.log(`Повторная отправка запроса ${requestId}`);
      alert(`Повторная отправка запроса ${requestId} (заглушка)`);
    },

    viewResponse(responseId) {
      console.log(`Просмотр ответа ${responseId}`);
      alert(`Просмотр ответа ${responseId} (заглушка)`);
    },

    downloadResponse(responseId) {
      console.log(`Скачивание ответа ${responseId}`);
      alert(`Скачивание ответа ${responseId} (заглушка)`);
    },

    exportResponses() {
      console.log('Экспорт ответов');
      alert('Экспорт ответов (заглушка)');
    },

    viewService(serviceId) {
      console.log(`Просмотр услуги ${serviceId}`);
      alert(`Просмотр услуги ${serviceId} (заглушка)`);
    },

    viewDepartment(departmentId) {
      console.log(`Просмотр органа власти ${departmentId}`);
      alert(`Просмотр органа власти ${departmentId} (заглушка)`);
    },

    testConnection(departmentId) {
      console.log(`Проверка связи с органом ${departmentId}`);
      alert(`Проверка связи с органом ${departmentId} (заглушка)`);
    },

    // Вспомогательные методы
    getStatusBadgeClass(status) {
      const classes = {
        pending: 'bg-warning',
        completed: 'bg-success',
        error: 'bg-danger',
        processing: 'bg-primary'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusText(status) {
      const texts = {
        pending: 'Ожидает обработки',
        completed: 'Обработан',
        error: 'Ошибка',
        processing: 'В обработке'
      };
      return texts[status] || status;
    },

    getResponseStatusBadgeClass(status) {
      const classes = {
        success: 'bg-success',
        error: 'bg-danger',
        pending: 'bg-warning'
      };
      return classes[status] || 'bg-secondary';
    },

    getResponseStatusText(status) {
      const texts = {
        success: 'Успешно',
        error: 'Ошибка',
        pending: 'В обработке'
      };
      return texts[status] || status;
    },

    getServiceIcon(category) {
      const icons = {
        tax: 'fas fa-money-bill-wave text-success',
        civil: 'fas fa-user-check text-primary',
        traffic: 'fas fa-car text-warning',
        social: 'fas fa-heart text-danger'
      };
      return icons[category] || 'fas fa-cog text-secondary';
    },

    getDepartmentTypeBadgeClass(type) {
      const classes = {
        federal: 'bg-primary',
        regional: 'bg-success',
        municipal: 'bg-info'
      };
      return classes[type] || 'bg-secondary';
    },

    getDepartmentTypeText(type) {
      const texts = {
        federal: 'Федеральный',
        regional: 'Региональный',
        municipal: 'Муниципальный'
      };
      return texts[type] || type;
    },

    getEventIcon(type) {
      const icons = {
        request_sent: 'fas fa-paper-plane text-primary',
        response_received: 'fas fa-inbox text-success',
        error: 'fas fa-exclamation-triangle text-danger'
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
    console.log('Компонента АСУР СМЭВ инициализирована');
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

.bg-primary {
  background-color: #007bff !important;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
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