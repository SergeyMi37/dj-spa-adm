<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-exchange-alt"></i> УСПП ЕАИСТ</h2>
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
              @click="createNeed" 
              class="btn btn-success btn-sm"
            >
              <i class="fas fa-plus"></i>
              Новая потребность
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
              Универсальный Сервис Передачи Потребностей ЕАИСТ
            </h5>
            <p class="card-text">
              УСПП ЕАИСТ обеспечивает единый интерфейс для передачи потребностей в товарах, 
              работах и услугах между заказчиками и поставщиками через Единую автоматизированную 
              информационную систему торгов. Система автоматизирует процесс выявления потребностей 
              и их передачи на электронные торговые площадки.
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
                <h3 class="mb-0">{{ stats.totalNeeds }}</h3>
                <p class="mb-0">Всего потребностей</p>
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
                <h3 class="mb-0">{{ stats.transferredToday }}</h3>
                <p class="mb-0">Передано сегодня</p>
              </div>
              <i class="fas fa-paper-plane fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ stats.pendingTransfer }}</h3>
                <p class="mb-0">В ожидании передачи</p>
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
                <h3 class="mb-0">{{ stats.successRate }}%</h3>
                <p class="mb-0">Успешность передачи</p>
              </div>
              <i class="fas fa-check-circle fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации УСПП ЕАИСТ -->
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
              @click="activeSection = 'needs'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'needs' }]"
            >
              <i class="fas fa-clipboard-list me-2"></i>
              Потребности
            </button>
            <button 
              @click="activeSection = 'transfer'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'transfer' }]"
            >
              <i class="fas fa-exchange-alt me-2"></i>
              Передача в ЕАИСТ
            </button>
            <button 
              @click="activeSection = 'templates'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'templates' }]"
            >
              <i class="fas fa-file-alt me-2"></i>
              Шаблоны
            </button>
            <button 
              @click="activeSection = 'monitoring'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'monitoring' }]"
            >
              <i class="fas fa-chart-line me-2"></i>
              Мониторинг
            </button>
            <button 
              @click="activeSection = 'integration'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'integration' }]"
            >
              <i class="fas fa-plug me-2"></i>
              Интеграция
            </button>
            <button 
              @click="activeSection = 'reports'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'reports' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Отчеты
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Потребности -->
        <div v-if="activeSection === 'needs'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-clipboard-list"></i>
              Управление потребностями
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по названию или коду..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="needFilter = 'all'"
                  :class="['btn', needFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="needFilter = 'new'"
                  :class="['btn', needFilter === 'new' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Новые
                </button>
                <button 
                  @click="needFilter = 'transferred'"
                  :class="['btn', needFilter === 'transferred' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Переданные
                </button>
                <button 
                  @click="needFilter = 'error'"
                  :class="['btn', needFilter === 'error' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Ошибочные
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Дата создания</th>
                    <th>Наименование</th>
                    <th>Код ОКВЭД</th>
                    <th>Сумма</th>
                    <th>Статус передачи</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="need in filteredNeeds" :key="need.id" :class="getNeedPriorityClass(need.priority)">
                    <td><strong>#{{ need.id }}</strong></td>
                    <td>
                      <small>{{ formatDate(need.created_at) }}</small>
                    </td>
                    <td>
                      <strong>{{ need.name }}</strong>
                      <br>
                      <small class="text-muted">{{ need.description.substring(0, 50) }}{{ need.description.length > 50 ? '...' : '' }}</small>
                    </td>
                    <td>
                      <span class="badge bg-info">{{ need.okved }}</span>
                    </td>
                    <td>
                      <strong>{{ need.amount.toLocaleString('ru-RU') }} ₽</strong>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getTransferStatusBadgeClass(need.transfer_status)]"
                      >
                        {{ getTransferStatusText(need.transfer_status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewNeed(need.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="editNeed(need.id)"
                          class="btn btn-outline-warning"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="transferNeed(need.id)"
                          v-if="need.transfer_status === 'new'"
                          class="btn btn-outline-success"
                          title="Передать в ЕАИСТ"
                        >
                          <i class="fas fa-exchange-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredNeeds.length === 0" class="text-center py-4">
              <i class="fas fa-clipboard-list fa-3x text-muted mb-3"></i>
              <p class="text-muted">Потребности не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Передача в ЕАИСТ -->
        <div v-if="activeSection === 'transfer'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-exchange-alt"></i>
              Передача потребностей в ЕАИСТ
            </h6>
          </div>
          <div class="card-body">
            <div class="alert alert-info" role="alert">
              <h6><i class="fas fa-info-circle"></i> Статус интеграции с ЕАИСТ</h6>
              <p class="mb-2">Последняя синхронизация: {{ formatDateTime(lastSync) }}</p>
              <div class="progress">
                <div 
                  class="progress-bar bg-success" 
                  role="progressbar" 
                  :style="`width: ${syncProgress}%`"
                >
                  {{ syncProgress }}%
                </div>
              </div>
            </div>

            <div class="mb-3">
              <h6>Очередь передачи</h6>
              <div v-if="transferQueue.length === 0" class="text-center py-3">
                <i class="fas fa-inbox fa-2x text-muted mb-2"></i>
                <p class="text-muted">Очередь передачи пуста</p>
              </div>
              <div v-else>
                <div v-for="item in transferQueue" :key="item.id" class="card mb-2">
                  <div class="card-body p-3">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <strong>#{{ item.need_id }}</strong> - {{ item.need_name }}
                        <br>
                        <small class="text-muted">{{ formatTime(item.queued_at) }}</small>
                      </div>
                      <div>
                        <span 
                          :class="['badge', getQueueStatusBadgeClass(item.status)]"
                        >
                          {{ getQueueStatusText(item.status) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Шаблоны -->
        <div v-if="activeSection === 'templates'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-file-alt"></i>
              Шаблоны потребностей
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-end">
              <button 
                @click="createTemplate"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Создать шаблон
              </button>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3" v-for="template in templates" :key="template.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i class="fas fa-file-alt text-primary me-2"></i>
                      {{ template.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ template.description }}</small>
                    </p>
                    <div class="mb-2">
                      <small class="text-muted">
                        <i class="fas fa-tag me-1"></i>
                        {{ template.category }}
                      </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">
                        Создан: {{ formatDate(template.created_at) }}
                      </small>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="useTemplate(template.id)"
                          class="btn btn-outline-primary"
                          title="Использовать"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                        <button 
                          @click="editTemplate(template.id)"
                          class="btn btn-outline-warning"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="deleteTemplate(template.id)"
                          class="btn btn-outline-danger"
                          title="Удалить"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="templates.length === 0" class="text-center py-4">
              <i class="fas fa-file-alt fa-3x text-muted mb-3"></i>
              <p class="text-muted">Шаблоны не найдены</p>
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
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика передачи потребностей</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="transferChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Статистика по категориям</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="category in categoryStats" :key="category.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ category.name }}</span>
                        <span class="badge bg-secondary">{{ category.count }}</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :class="category.color"
                          :style="`width: ${(category.count / stats.totalNeeds) * 100}%`"
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

        <!-- Раздел Интеграция -->
        <div v-if="activeSection === 'integration'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-plug"></i>
              Настройки интеграции с ЕАИСТ
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Подключение к ЕАИСТ</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <label class="form-label">URL сервиса ЕАИСТ</label>
                      <input 
                        v-model="integrationSettings.eaistUrl"
                        type="text" 
                        class="form-control" 
                        placeholder="https://eaist-service.ru/api"
                      >
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Токен доступа</label>
                      <div class="input-group">
                        <input 
                          v-model="integrationSettings.accessToken"
                          :type="showToken ? 'text' : 'password'" 
                          class="form-control" 
                          placeholder="Введите токен"
                        >
                        <div class="input-group-append">
                          <button 
                            @click="showToken = !showToken"
                            class="btn btn-outline-secondary" 
                            type="button"
                          >
                            <i :class="showToken ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="mb-3">
                      <div class="form-check">
                        <input 
                          v-model="integrationSettings.autoSync"
                          class="form-check-input" 
                          type="checkbox"
                          id="autoSync"
                        >
                        <label class="form-check-label" for="autoSync">
                          Автоматическая синхронизация
                        </label>
                      </div>
                    </div>
                    <button 
                      @click="testConnection"
                      class="btn btn-outline-primary btn-block"
                    >
                      <i class="fas fa-plug me-2"></i>
                      Проверить соединение
                    </button>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Статус подключения</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Статус:</span>
                        <span 
                          :class="connectionStatus.connected ? 'text-success' : 'text-danger'"
                          class="fw-bold"
                        >
                          {{ connectionStatus.connected ? 'Подключено' : 'Отключено' }}
                        </span>
                      </div>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Время ответа:</span>
                        <span>{{ connectionStatus.responseTime }} мс</span>
                      </div>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Последняя проверка:</span>
                        <small>{{ formatDateTime(connectionStatus.lastCheck) }}</small>
                      </div>
                    </div>
                    <div class="alert" :class="connectionStatus.connected ? 'alert-success' : 'alert-danger'">
                      {{ connectionStatus.message }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Отчеты -->
        <div v-if="activeSection === 'reports'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Отчеты и аналитика
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6>Период отчета</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <label class="form-label">С:</label>
                      <input 
                        v-model="reportSettings.dateFrom"
                        type="date" 
                        class="form-control form-control-sm"
                      >
                    </div>
                    <div class="mb-3">
                      <label class="form-label">По:</label>
                      <input 
                        v-model="reportSettings.dateTo"
                        type="date" 
                        class="form-control form-control-sm"
                      >
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Формат:</label>
                      <select v-model="reportSettings.format" class="form-control form-control-sm">
                        <option value="pdf">PDF</option>
                        <option value="excel">Excel</option>
                        <option value="csv">CSV</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-8">
                <div class="card">
                  <div class="card-header">
                    <h6>Доступные отчеты</h6>
                  </div>
                  <div class="card-body">
                    <div class="list-group">
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Отчет о передаче потребностей</h6>
                          <small class="text-muted">Детальная информация о всех переданных потребностях</small>
                        </div>
                        <button 
                          @click="generateReport('transfer')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-download"></i>
                        </button>
                      </div>
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Анализ эффективности</h6>
                          <small class="text-muted">Статистика успешности передачи потребностей</small>
                        </div>
                        <button 
                          @click="generateReport('efficiency')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-download"></i>
                        </button>
                      </div>
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Сводный отчет</h6>
                          <small class="text-muted">Общая статистика по всем показателям УСПП</small>
                        </div>
                        <button 
                          @click="generateReport('summary')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-download"></i>
                        </button>
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
  name: 'USPP',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'needs',
      searchQuery: '',
      needFilter: 'all',
      showToken: false,
      
      // Статистика
      stats: {
        totalNeeds: 1247,
        transferredToday: 23,
        pendingTransfer: 12,
        successRate: 94
      },

      // Потребности
      needs: [
        {
          id: 1001,
          created_at: new Date('2024-01-15T10:30:00'),
          name: 'Поставка офисной мебели',
          description: 'Закупка столов, стульев и шкафов для оборудования офисных помещений',
          okved: '31.01',
          amount: 2500000,
          priority: 'high',
          transfer_status: 'new'
        },
        {
          id: 1002,
          created_at: new Date('2024-01-15T09:15:00'),
          name: 'IT оборудование',
          description: 'Компьютеры, серверы и сетевое оборудование',
          okved: '26.20',
          amount: 1500000,
          priority: 'medium',
          transfer_status: 'transferred'
        },
        {
          id: 1003,
          created_at: new Date('2024-01-15T08:45:00'),
          name: 'Клининговые услуги',
          description: 'Уборка и содержание помещений',
          okved: '81.21',
          amount: 500000,
          priority: 'low',
          transfer_status: 'error'
        }
      ],

      // Очередь передачи
      transferQueue: [
        {
          id: 1,
          need_id: 1001,
          need_name: 'Поставка офисной мебели',
          status: 'processing',
          queued_at: new Date('2024-01-15T10:35:00')
        }
      ],

      // Шаблоны
      templates: [
        {
          id: 1,
          name: 'Офисная мебель',
          description: 'Шаблон для закупки офисной мебели',
          category: 'Мебель',
          created_at: new Date('2024-01-10')
        },
        {
          id: 2,
          name: 'IT оборудование',
          description: 'Шаблон для закупки компьютерной техники',
          category: 'IT',
          created_at: new Date('2024-01-08')
        }
      ],

      // Статистика по категориям
      categoryStats: [
        { name: 'Мебель', count: 125, color: 'bg-primary' },
        { name: 'IT оборудование', count: 89, color: 'bg-success' },
        { name: 'Услуги', count: 67, color: 'bg-warning' },
        { name: 'Строительство', count: 45, color: 'bg-danger' },
        { name: 'Прочие', count: 23, color: 'bg-secondary' }
      ],

      // Последние события
      recentEvents: [
        {
          id: 1,
          type: 'need_created',
          message: 'Создана новая потребность #1001',
          timestamp: new Date('2024-01-15T10:30:00')
        },
        {
          id: 2,
          type: 'transfer_success',
          message: 'Потребность #1002 успешно передана в ЕАИСТ',
          timestamp: new Date('2024-01-15T09:20:00')
        },
        {
          id: 3,
          type: 'transfer_error',
          message: 'Ошибка передачи потребности #1003',
          timestamp: new Date('2024-01-15T08:50:00')
        }
      ],

      // Настройки интеграции
      integrationSettings: {
        eaistUrl: 'https://eaist-service.ru/api',
        accessToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        autoSync: true
      },

      // Статус подключения
      connectionStatus: {
        connected: true,
        responseTime: 245,
        lastCheck: new Date(),
        message: 'Подключение к ЕАИСТ активно'
      },

      // Настройки отчетов
      reportSettings: {
        dateFrom: '2024-01-01',
        dateTo: '2024-01-31',
        format: 'pdf'
      },

      // Синхронизация
      lastSync: new Date(),
      syncProgress: 100
    };
  },
  computed: {
    filteredNeeds() {
      let filtered = this.needs;
      
      if (this.searchQuery) {
        filtered = filtered.filter(need => 
          need.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          need.description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          need.id.toString().includes(this.searchQuery)
        );
      }
      
      if (this.needFilter !== 'all') {
        if (this.needFilter === 'new') {
          filtered = filtered.filter(need => need.transfer_status === 'new');
        } else if (this.needFilter === 'transferred') {
          filtered = filtered.filter(need => need.transfer_status === 'transferred');
        } else if (this.needFilter === 'error') {
          filtered = filtered.filter(need => need.transfer_status === 'error');
        }
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
        console.log('Данные УСПП ЕАИСТ обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    createNeed() {
      console.log('Создание новой потребности');
      alert('Создание новой потребности (заглушка)');
    },

    viewNeed(needId) {
      console.log(`Просмотр потребности ${needId}`);
      alert(`Просмотр потребности ${needId} (заглушка)`);
    },

    editNeed(needId) {
      console.log(`Редактирование потребности ${needId}`);
      alert(`Редактирование потребности ${needId} (заглушка)`);
    },

    transferNeed(needId) {
      const need = this.needs.find(n => n.id === needId);
      if (need) {
        need.transfer_status = 'transferred';
        // Добавляем в очередь передачи
        this.transferQueue.push({
          id: Date.now(),
          need_id: needId,
          need_name: need.name,
          status: 'processing',
          queued_at: new Date()
        });
      }
      console.log(`Передача потребности ${needId} в ЕАИСТ`);
    },

    createTemplate() {
      console.log('Создание нового шаблона');
      alert('Создание нового шаблона (заглушка)');
    },

    useTemplate(templateId) {
      console.log(`Использование шаблона ${templateId}`);
      alert(`Использование шаблона ${templateId} (заглушка)`);
    },

    editTemplate(templateId) {
      console.log(`Редактирование шаблона ${templateId}`);
      alert(`Редактирование шаблона ${templateId} (заглушка)`);
    },

    deleteTemplate(templateId) {
      if (confirm('Вы уверены, что хотите удалить этот шаблон?')) {
        const index = this.templates.findIndex(t => t.id === templateId);
        if (index > -1) {
          this.templates.splice(index, 1);
        }
      }
      console.log(`Удаление шаблона ${templateId}`);
    },

    testConnection() {
      this.loading = true;
      setTimeout(() => {
        this.connectionStatus.connected = true;
        this.connectionStatus.responseTime = Math.floor(Math.random() * 500) + 100;
        this.connectionStatus.lastCheck = new Date();
        this.connectionStatus.message = 'Подключение к ЕАИСТ активно';
        this.loading = false;
      }, 2000);
    },

    generateReport(reportType) {
      console.log(`Генерация отчета типа: ${reportType}`);
      alert(`Генерация отчета "${reportType}" (заглушка)`);
    },

    // Вспомогательные методы
    getNeedPriorityClass(priority) {
      return priority === 'high' ? 'table-danger' : priority === 'medium' ? 'table-warning' : '';
    },

    getTransferStatusBadgeClass(status) {
      const classes = {
        new: 'bg-secondary',
        transferred: 'bg-success',
        error: 'bg-danger',
        processing: 'bg-primary'
      };
      return classes[status] || 'bg-secondary';
    },

    getTransferStatusText(status) {
      const texts = {
        new: 'Новая',
        transferred: 'Передана',
        error: 'Ошибка',
        processing: 'В обработке'
      };
      return texts[status] || status;
    },

    getQueueStatusBadgeClass(status) {
      const classes = {
        queued: 'bg-info',
        processing: 'bg-warning',
        completed: 'bg-success',
        failed: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getQueueStatusText(status) {
      const texts = {
        queued: 'В очереди',
        processing: 'Обработка',
        completed: 'Завершено',
        failed: 'Ошибка'
      };
      return texts[status] || status;
    },

    getEventIcon(type) {
      const icons = {
        need_created: 'fas fa-plus text-success',
        transfer_success: 'fas fa-check text-success',
        transfer_error: 'fas fa-exclamation-triangle text-danger'
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
    console.log('Компонента УСПП ЕАИСТ инициализирована');
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

.fw-bold {
  font-weight: 600;
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