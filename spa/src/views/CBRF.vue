<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-university"></i> Центральный банк РФ</h2>
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
              <i class="fas fa-chart-line"></i>
              Отчет
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
              Центральный банк Российской Федерации
            </h5>
            <p class="card-text">
              ЦБ РФ осуществляет единую государственную денежно-кредитную политику, 
              обеспечивает стабильность банковской системы, проводит банковские операции 
              для обслуживания государственных финансов и управляет золотовалютными резервами.
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
                <h3 class="mb-0">{{ keyMetrics.keyRate }}%</h3>
                <p class="mb-0">Ключевая ставка</p>
              </div>
              <i class="fas fa-percentage fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.inflation }}%</h3>
                <p class="mb-0">Инфляция</p>
              </div>
              <i class="fas fa-chart-line fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.reserves }} трлн ₽</h3>
                <p class="mb-0">Золотовалютные резервы</p>
              </div>
              <i class="fas fa-coins fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.exchangeRate }}</h3>
                <p class="mb-0">Курс USD/RUB</p>
              </div>
              <i class="fas fa-exchange-alt fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации ЦБ РФ -->
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
              <i class="fas fa-chart-pie me-2"></i>
              Мониторинг
            </button>
            <button 
              @click="activeSection = 'monetary'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'monetary' }]"
            >
              <i class="fas fa-coins me-2"></i>
              Денежно-кредитная политика
            </button>
            <button 
              @click="activeSection = 'banks'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'banks' }]"
            >
              <i class="fas fa-university me-2"></i>
              Банки
            </button>
            <button 
              @click="activeSection = 'payments'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'payments' }]"
            >
              <i class="fas fa-credit-card me-2"></i>
              Платежные системы
            </button>
            <button 
              @click="activeSection = 'analytics'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'analytics' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Аналитика
            </button>
            <button 
              @click="activeSection = 'supervision'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'supervision' }]"
            >
              <i class="fas fa-shield-alt me-2"></i>
              Надзор
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Мониторинг -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-pie"></i>
              Общий мониторинг
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика ключевой ставки</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="rateChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Курсы валют (сегодня)</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="rate in exchangeRates" :key="rate.currency" class="d-flex justify-content-between mb-2">
                      <span>{{ rate.currency }}</span>
                      <div class="text-right">
                        <span class="fw-bold">{{ rate.rate }}</span>
                        <small 
                          :class="rate.change >= 0 ? 'text-success' : 'text-danger'"
                          class="ms-2"
                        >
                          <i :class="rate.change >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                          {{ Math.abs(rate.change) }}%
                        </small>
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
                    <h6>Последние события ЦБ РФ</h6>
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

        <!-- Раздел Денежно-кредитная политика -->
        <div v-if="activeSection === 'monetary'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-coins"></i>
              Денежно-кредитная политика
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div>
                <select v-model="monetaryFilter" class="form-control form-control-sm" style="width: 200px; display: inline-block;">
                  <option value="all">Все операции</option>
                  <option value="interventions">Валютные интервенции</option>
                  <option value="liquidity">Управление ликвидностью</option>
                  <option value="reserve_requirements">Резервные требования</option>
                </select>
              </div>
              <button 
                @click="newOperation"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Новая операция
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Дата</th>
                    <th>Тип операции</th>
                    <th>Объем</th>
                    <th>Статус</th>
                    <th>Влияние на ставку</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="operation in filteredMonetaryOperations" :key="operation.id">
                    <td>
                      <small>{{ formatDate(operation.date) }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getOperationTypeBadgeClass(operation.type)">
                        {{ getOperationTypeText(operation.type) }}
                      </span>
                    </td>
                    <td>
                      <strong>{{ operation.amount.toLocaleString('ru-RU') }} ₽</strong>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getStatusBadgeClass(operation.status)]"
                      >
                        {{ getStatusText(operation.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ operation.rate_impact > 0 ? '+' : '' }}{{ operation.rate_impact }} п.п.</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewOperation(operation.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="editOperation(operation.id)"
                          class="btn btn-outline-warning"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredMonetaryOperations.length === 0" class="text-center py-4">
              <i class="fas fa-coins fa-3x text-muted mb-3"></i>
              <p class="text-muted">Операции не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Банки -->
        <div v-if="activeSection === 'banks'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-university"></i>
              Банки
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по названию..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="bankFilter = 'all'"
                  :class="['btn', bankFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="bankFilter = 'system'"
                  :class="['btn', bankFilter === 'system' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Системно важные
                </button>
                <button 
                  @click="bankFilter = 'license'"
                  :class="['btn', bankFilter === 'license' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  С лицензией
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Регистрационный номер</th>
                    <th>Категория</th>
                    <th>Капитал</th>
                    <th>Статус лицензии</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="bank in filteredBanks" :key="bank.id">
                    <td>
                      <strong>{{ bank.name }}</strong>
                      <br>
                      <small class="text-muted">{{ bank.short_name }}</small>
                    </td>
                    <td>{{ bank.reg_number }}</td>
                    <td>
                      <span 
                        :class="['badge', getBankCategoryBadgeClass(bank.category)]"
                      >
                        {{ getBankCategoryText(bank.category) }}
                      </span>
                    </td>
                    <td>
                      <strong>{{ bank.capital.toLocaleString('ru-RU') }} млрд ₽</strong>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getLicenseStatusBadgeClass(bank.license_status)]"
                      >
                        {{ getLicenseStatusText(bank.license_status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewBank(bank.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="inspectBank(bank.id)"
                          class="btn btn-outline-warning"
                          title="Инспекция"
                        >
                          <i class="fas fa-search"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredBanks.length === 0" class="text-center py-4">
              <i class="fas fa-university fa-3x text-muted mb-3"></i>
              <p class="text-muted">Банки не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Платежные системы -->
        <div v-if="activeSection === 'payments'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-credit-card"></i>
              Платежные системы
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="system in paymentSystems" :key="system.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i :class="getPaymentSystemIcon(system.type)" class="me-2"></i>
                      {{ system.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ system.description }}</small>
                    </p>
                    <div class="mb-2">
                      <div class="d-flex justify-content-between">
                        <small class="text-muted">Операций в день:</small>
                        <strong>{{ system.daily_operations.toLocaleString('ru-RU') }}</strong>
                      </div>
                    </div>
                    <div class="mb-2">
                      <div class="d-flex justify-content-between">
                        <small class="text-muted">Объем транзакций:</small>
                        <strong>{{ system.volume.toLocaleString('ru-RU') }} млрд ₽</strong>
                      </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <span 
                        :class="['badge', getSystemStatusBadgeClass(system.status)]"
                      >
                        {{ getSystemStatusText(system.status) }}
                      </span>
                      <small class="text-muted">Загрузка: {{ system.load }}%</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="paymentSystems.length === 0" class="text-center py-4">
              <i class="fas fa-credit-card fa-3x text-muted mb-3"></i>
              <p class="text-muted">Платежные системы не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Аналитика -->
        <div v-if="activeSection === 'analytics'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Аналитика и статистика
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика инфляции</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="inflationChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Ключевые показатели</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="metric in keyIndicators" :key="metric.name" class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>{{ metric.name }}</span>
                        <strong>{{ metric.value }}</strong>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :class="metric.color"
                          :style="`width: ${metric.percentage}%`"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Надзор -->
        <div v-if="activeSection === 'supervision'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-shield-alt"></i>
              Банковский надзор
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h3 class="text-warning">{{ supervisionStats.riskBanks }}</h3>
                    <p class="mb-0">Банков под надзором</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h3 class="text-danger">{{ supervisionStats.violations }}</h3>
                    <p class="mb-0">Выявленных нарушений</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h3 class="text-success">{{ supervisionStats.resolved }}</h3>
                    <p class="mb-0">Устраненных нарушений</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Банк</th>
                    <th>Тип нарушения</th>
                    <th>Дата выявления</th>
                    <th>Статус</th>
                    <th>Срок устранения</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="violation in violations" :key="violation.id">
                    <td>{{ violation.bank_name }}</td>
                    <td>{{ violation.violation_type }}</td>
                    <td>
                      <small>{{ formatDate(violation.detection_date) }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getViolationStatusBadgeClass(violation.status)]"
                      >
                        {{ getViolationStatusText(violation.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ formatDate(violation.deadline) }}</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewViolation(violation.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="markResolved(violation.id)"
                          v-if="violation.status === 'open'"
                          class="btn btn-outline-success"
                          title="Отметить устраненным"
                        >
                          <i class="fas fa-check"></i>
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
  name: 'CBRF',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      searchQuery: '',
      monetaryFilter: 'all',
      bankFilter: 'all',
      
      // Ключевые показатели
      keyMetrics: {
        keyRate: 16.0,
        inflation: 7.5,
        reserves: 603.2,
        exchangeRate: 89.45
      },

      // Валютные курсы
      exchangeRates: [
        { currency: 'USD/RUB', rate: 89.45, change: 0.15 },
        { currency: 'EUR/RUB', rate: 97.32, change: -0.23 },
        { currency: 'GBP/RUB', rate: 113.78, change: 0.08 },
        { currency: 'CNY/RUB', rate: 12.34, change: 0.02 }
      ],

      // Последние события
      recentEvents: [
        {
          id: 1,
          type: 'rate_change',
          message: 'Изменение ключевой ставки до 16.0%',
          timestamp: new Date('2024-01-15T14:30:00')
        },
        {
          id: 2,
          type: 'intervention',
          message: 'Валютная интервенция на сумму 5 млрд руб.',
          timestamp: new Date('2024-01-15T13:15:00')
        },
        {
          id: 3,
          type: 'report',
          message: 'Опубликован ежемесячный обзор банковского сектора',
          timestamp: new Date('2024-01-15T10:00:00')
        }
      ],

      // Денежно-кредитные операции
      monetaryOperations: [
        {
          id: 1,
          date: new Date('2024-01-15'),
          type: 'interventions',
          amount: 5000000000,
          status: 'completed',
          rate_impact: -0.25
        },
        {
          id: 2,
          date: new Date('2024-01-14'),
          type: 'liquidity',
          amount: 25000000000,
          status: 'planned',
          rate_impact: 0
        }
      ],

      // Банки
      banks: [
        {
          id: 1,
          name: 'Сбербанк России',
          short_name: 'ПАО Сбербанк',
          reg_number: 1481,
          category: 'system',
          capital: 4785.2,
          license_status: 'active'
        },
        {
          id: 2,
          name: 'ВТБ',
          short_name: 'Банк ВТБ (ПАО)',
          reg_number: 1000,
          category: 'system',
          capital: 1234.5,
          license_status: 'active'
        },
        {
          id: 3,
          name: 'Газпромбанк',
          short_name: 'Банк ГПБ (АО)',
          reg_number: 354,
          category: 'large',
          capital: 892.3,
          license_status: 'active'
        }
      ],

      // Платежные системы
      paymentSystems: [
        {
          id: 1,
          name: 'МИР',
          type: 'card',
          description: 'Национальная платежная система',
          status: 'operational',
          daily_operations: 12500000,
          volume: 45.6,
          load: 78
        },
        {
          id: 2,
          name: 'Банк России',
          type: 'settlement',
          description: 'Система валовых расчетов',
          status: 'operational',
          daily_operations: 2500000,
          volume: 234.7,
          load: 65
        }
      ],

      // Ключевые показатели для аналитики
      keyIndicators: [
        { name: 'Стабильность банков', value: '89%', percentage: 89, color: 'bg-success' },
        { name: 'Качество кредитного портфеля', value: '76%', percentage: 76, color: 'bg-warning' },
        { name: 'Ликвидность', value: '92%', percentage: 92, color: 'bg-success' },
        { name: 'Капитализация', value: '84%', percentage: 84, color: 'bg-info' }
      ],

      // Статистика надзора
      supervisionStats: {
        riskBanks: 23,
        violations: 45,
        resolved: 38
      },

      // Нарушения
      violations: [
        {
          id: 1,
          bank_name: 'ПАО Сбербанк',
          violation_type: 'Требования к капиталу',
          detection_date: new Date('2024-01-10'),
          status: 'resolved',
          deadline: new Date('2024-02-15')
        },
        {
          id: 2,
          bank_name: 'Банк ВТБ (ПАО)',
          violation_type: 'Валютное законодательство',
          detection_date: new Date('2024-01-12'),
          status: 'open',
          deadline: new Date('2024-02-20')
        }
      ]
    };
  },
  computed: {
    filteredMonetaryOperations() {
      let filtered = this.monetaryOperations;
      
      if (this.monetaryFilter !== 'all') {
        filtered = filtered.filter(operation => operation.type === this.monetaryFilter);
      }
      
      return filtered;
    },

    filteredBanks() {
      let filtered = this.banks;
      
      if (this.searchQuery) {
        filtered = filtered.filter(bank => 
          bank.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          bank.short_name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
      if (this.bankFilter !== 'all') {
        if (this.bankFilter === 'system') {
          filtered = filtered.filter(bank => bank.category === 'system');
        } else if (this.bankFilter === 'license') {
          filtered = filtered.filter(bank => bank.license_status === 'active');
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
        console.log('Данные ЦБ РФ обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    generateReport() {
      console.log('Генерация отчета ЦБ РФ');
      alert('Генерация отчета ЦБ РФ (заглушка)');
    },

    newOperation() {
      console.log('Создание новой денежно-кредитной операции');
      alert('Создание новой денежно-кредитной операции (заглушка)');
    },

    viewOperation(operationId) {
      console.log(`Просмотр операции ${operationId}`);
      alert(`Просмотр операции ${operationId} (заглушка)`);
    },

    editOperation(operationId) {
      console.log(`Редактирование операции ${operationId}`);
      alert(`Редактирование операции ${operationId} (заглушка)`);
    },

    viewBank(bankId) {
      console.log(`Просмотр банка ${bankId}`);
      alert(`Просмотр банка ${bankId} (заглушка)`);
    },

    inspectBank(bankId) {
      console.log(`Инспекция банка ${bankId}`);
      alert(`Инспекция банка ${bankId} (заглушка)`);
    },

    viewViolation(violationId) {
      console.log(`Просмотр нарушения ${violationId}`);
      alert(`Просмотр нарушения ${violationId} (заглушка)`);
    },

    markResolved(violationId) {
      const violation = this.violations.find(v => v.id === violationId);
      if (violation) {
        violation.status = 'resolved';
      }
      console.log(`Нарушение ${violationId} отмечено как устраненное`);
    },

    // Вспомогательные методы
    getEventIcon(type) {
      const icons = {
        rate_change: 'fas fa-percentage text-primary',
        intervention: 'fas fa-coins text-warning',
        report: 'fas fa-file-alt text-info'
      };
      return icons[type] || 'fas fa-info-circle text-secondary';
    },

    getOperationTypeBadgeClass(type) {
      const classes = {
        interventions: 'bg-warning',
        liquidity: 'bg-primary',
        reserve_requirements: 'bg-info'
      };
      return classes[type] || 'bg-secondary';
    },

    getOperationTypeText(type) {
      const texts = {
        interventions: 'Валютные интервенции',
        liquidity: 'Управление ликвидностью',
        reserve_requirements: 'Резервные требования'
      };
      return texts[type] || type;
    },

    getStatusBadgeClass(status) {
      const classes = {
        completed: 'bg-success',
        planned: 'bg-info',
        cancelled: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusText(status) {
      const texts = {
        completed: 'Завершена',
        planned: 'Запланирована',
        cancelled: 'Отменена'
      };
      return texts[status] || status;
    },

    getBankCategoryBadgeClass(category) {
      const classes = {
        system: 'bg-danger',
        large: 'bg-warning',
        medium: 'bg-info',
        small: 'bg-secondary'
      };
      return classes[category] || 'bg-secondary';
    },

    getBankCategoryText(category) {
      const texts = {
        system: 'Системно важный',
        large: 'Крупный',
        medium: 'Средний',
        small: 'Малый'
      };
      return texts[category] || category;
    },

    getLicenseStatusBadgeClass(status) {
      const classes = {
        active: 'bg-success',
        suspended: 'bg-warning',
        revoked: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getLicenseStatusText(status) {
      const texts = {
        active: 'Действующая',
        suspended: 'Приостановлена',
        revoked: 'Отозвана'
      };
      return texts[status] || status;
    },

    getPaymentSystemIcon(type) {
      const icons = {
        card: 'fas fa-credit-card text-primary',
        settlement: 'fas fa-exchange-alt text-success',
        digital: 'fas fa-mobile-alt text-info'
      };
      return icons[type] || 'fas fa-cog text-secondary';
    },

    getSystemStatusBadgeClass(status) {
      const classes = {
        operational: 'bg-success',
        maintenance: 'bg-warning',
        outage: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getSystemStatusText(status) {
      const texts = {
        operational: 'Работает',
        maintenance: 'Техобслуживание',
        outage: 'Недоступна'
      };
      return texts[status] || status;
    },

    getViolationStatusBadgeClass(status) {
      const classes = {
        open: 'bg-danger',
        in_progress: 'bg-warning',
        resolved: 'bg-success'
      };
      return classes[status] || 'bg-secondary';
    },

    getViolationStatusText(status) {
      const texts = {
        open: 'Открыто',
        in_progress: 'В работе',
        resolved: 'Устранено'
      };
      return texts[status] || status;
    },

    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleDateString('ru-RU');
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
    console.log('Компонента ЦБ РФ инициализирована');
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