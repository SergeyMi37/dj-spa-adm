<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-file-alt"></i> Отчеты УЗ</h2>
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
              @click="exportData" 
              class="btn btn-outline-success btn-sm"
            >
              <i class="fas fa-download"></i>
              Экспорт
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
              Отчеты Управления закупок
            </h5>
            <p class="card-text">
              Система управления отчетами Управления закупок предназначена для автоматизированного 
              формирования, мониторинга и анализа отчетных данных по государственным закупкам.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации Отчетов УЗ -->
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
              Дашборд
            </button>
            <button 
              @click="activeSection = 'procurements'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'procurements' }]"
            >
              <i class="fas fa-shopping-cart me-2"></i>
              Отчеты по закупкам
            </button>
            <button 
              @click="activeSection = 'contracts'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'contracts' }]"
            >
              <i class="fas fa-file-contract me-2"></i>
              Контракты и договоры
            </button>
            <button 
              @click="activeSection = 'suppliers'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'suppliers' }]"
            >
              <i class="fas fa-building me-2"></i>
              Анализ поставщиков
            </button>
            <button 
              @click="activeSection = 'budget'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'budget' }]"
            >
              <i class="fas fa-calculator me-2"></i>
              Бюджетный контроль
            </button>
            <button 
              @click="activeSection = 'analytics'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'analytics' }]"
            >
              <i class="fas fa-analytics me-2"></i>
              Аналитические отчеты
            </button>
            <button 
              @click="activeSection = 'templates'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'templates' }]"
            >
              <i class="fas fa-file me-2"></i>
              Шаблоны отчетов
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Дашборд -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Дашборд Управления закупок
            </h6>
          </div>
          <div class="card-body">
            <!-- Ключевые показатели -->
            <div class="row mb-4">
              <div class="col-md-3 mb-3">
                <div class="card bg-primary text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.totalProcurements }}</h4>
                        <small>Всего закупок</small>
                      </div>
                      <i class="fas fa-shopping-cart fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-success text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.totalAmount.toLocaleString('ru-RU') }} млн ₽</h4>
                        <small>Общая сумма</small>
                      </div>
                      <i class="fas fa-ruble-sign fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-info text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.savingsPercent }}%</h4>
                        <small>Экономия средств</small>
                      </div>
                      <i class="fas fa-chart-line fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-warning text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.activeSuppliers }}</h4>
                        <small>Активных поставщиков</small>
                      </div>
                      <i class="fas fa-building fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Графики и диаграммы -->
            <div class="row">
              <div class="col-md-6 mb-3">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Динамика закупок по месяцам</h6>
                  </div>
                  <div class="card-body">
                    <div class="text-center py-4">
                      <i class="fas fa-chart-bar fa-3x text-muted mb-3"></i>
                      <p class="text-muted">График динамики закупок</p>
                      <small class="text-muted">Общая сумма: {{ dashboardData.monthlyAmount }} млн ₽</small>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-6 mb-3">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Статус исполнения контрактов</h6>
                  </div>
                  <div class="card-body">
                    <div class="text-center py-4">
                      <i class="fas fa-chart-pie fa-3x text-muted mb-3"></i>
                      <p class="text-muted">Распределение контрактов</p>
                      <small class="text-muted">Всего контрактов: {{ dashboardData.totalContracts }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Отчеты по закупкам -->
        <div v-if="activeSection === 'procurements'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-shopping-cart"></i>
              Отчеты по закупкам
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по предмету закупки..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group">
                <button 
                  @click="generateReport"
                  class="btn btn-success btn-sm"
                >
                  <i class="fas fa-plus"></i>
                  Создать отчет
                </button>
                <button 
                  @click="exportProcurements"
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="fas fa-download"></i>
                  Экспорт
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Дата</th>
                    <th>Предмет закупки</th>
                    <th>Способ</th>
                    <th>Сумма</th>
                    <th>Экономия</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="procurement in filteredProcurements" :key="procurement.id">
                    <td>
                      <small>{{ formatDate(procurement.date) }}</small>
                    </td>
                    <td>{{ procurement.subject }}</td>
                    <td>
                      <small>{{ procurement.method }}</small>
                    </td>
                    <td class="text-right">
                      <strong>{{ procurement.amount.toLocaleString('ru-RU') }} ₽</strong>
                    </td>
                    <td class="text-right">
                      <span class="text-success">
                        {{ procurement.savings.toLocaleString('ru-RU') }} ₽
                      </span>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getProcurementStatusClass(procurement.status)]"
                      >
                        {{ getProcurementStatusText(procurement.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewProcurement(procurement.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="generateProcurementReport(procurement.id)"
                          class="btn btn-outline-success"
                          title="Создать отчет"
                        >
                          <i class="fas fa-file-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredProcurements.length === 0" class="text-center py-4">
              <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
              <p class="text-muted">Закупки не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Контракты и договоры -->
        <div v-if="activeSection === 'contracts'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-file-contract"></i>
              Контракты и договоры
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group" role="group">
                <button 
                  @click="contractFilter = 'all'"
                  :class="['btn', 'btn-sm', contractFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все контракты
                </button>
                <button 
                  @click="contractFilter = 'active'"
                  :class="['btn', 'btn-sm', contractFilter === 'active' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Активные
                </button>
                <button 
                  @click="contractFilter = 'expired'"
                  :class="['btn', 'btn-sm', contractFilter === 'expired' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Истекшие
                </button>
                <button 
                  @click="contractFilter = 'pending'"
                  :class="['btn', 'btn-sm', contractFilter === 'pending' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Ожидающие
                </button>
              </div>
              <button 
                @click="createContract"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Новый контракт
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Номер</th>
                    <th>Поставщик</th>
                    <th>Предмет</th>
                    <th>Сумма</th>
                    <th>Срок действия</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="contract in filteredContracts" :key="contract.id">
                    <td>
                      <strong>{{ contract.number }}</strong>
                    </td>
                    <td>{{ contract.supplier }}</td>
                    <td>
                      <small>{{ contract.subject }}</small>
                    </td>
                    <td class="text-right">
                      {{ contract.amount.toLocaleString('ru-RU') }} ₽
                    </td>
                    <td>
                      <small>{{ formatDate(contract.endDate) }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getContractStatusClass(contract.status)]"
                      >
                        {{ getContractStatusText(contract.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewContract(contract.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="generateContractReport(contract.id)"
                          class="btn btn-outline-success"
                          title="Отчет по контракту"
                        >
                          <i class="fas fa-file-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredContracts.length === 0" class="text-center py-4">
              <i class="fas fa-file-contract fa-3x text-muted mb-3"></i>
              <p class="text-muted">Контракты не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Анализ поставщиков -->
        <div v-if="activeSection === 'suppliers'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-building"></i>
              Анализ поставщиков
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="supplier in suppliers" :key="supplier.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i class="fas fa-building me-2"></i>
                      {{ supplier.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ supplier.category }}</small>
                    </p>
                    <div class="row">
                      <div class="col-6">
                        <small class="text-muted">Закупок:</small><br>
                        <strong>{{ supplier.procurements }}</strong>
                      </div>
                      <div class="col-6">
                        <small class="text-muted">Сумма:</small><br>
                        <strong>{{ supplier.totalAmount.toLocaleString('ru-RU') }} ₽</strong>
                      </div>
                    </div>
                    <div class="mt-2">
                      <small class="text-muted">Рейтинг:</small>
                      <div class="d-flex align-items-center">
                        <div class="progress flex-grow-1 me-2" style="height: 6px;">
                          <div 
                            class="progress-bar bg-success" 
                            :style="{ width: (supplier.rating * 20) + '%' }"
                          ></div>
                        </div>
                        <small>{{ supplier.rating }}/5</small>
                      </div>
                    </div>
                    <div class="mt-3">
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewSupplier(supplier.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="generateSupplierReport(supplier.id)"
                          class="btn btn-outline-success"
                          title="Отчет по поставщику"
                        >
                          <i class="fas fa-file-alt"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="suppliers.length === 0" class="text-center py-4">
              <i class="fas fa-building fa-3x text-muted mb-3"></i>
              <p class="text-muted">Поставщики не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Бюджетный контроль -->
        <div v-if="activeSection === 'budget'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-calculator"></i>
              Бюджетный контроль
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-4">
              <h6>Плановые и фактические расходы по статьям бюджета</h6>
              <div class="table-responsive">
                <table class="table table-hover table-sm">
                  <thead>
                    <tr>
                      <th>Статья бюджета</th>
                      <th class="text-right">План</th>
                      <th class="text-right">Факт</th>
                      <th class="text-right">Отклонение</th>
                      <th class="text-center">Статус</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="budget in budgetItems" :key="budget.id">
                      <td>{{ budget.category }}</td>
                      <td class="text-right">
                        {{ budget.planned.toLocaleString('ru-RU') }} ₽
                      </td>
                      <td class="text-right">
                        {{ budget.actual.toLocaleString('ru-RU') }} ₽
                      </td>
                      <td class="text-right">
                        <span 
                          :class="budget.deviation >= 0 ? 'text-danger' : 'text-success'"
                        >
                          {{ budget.deviation.toLocaleString('ru-RU') }} ₽
                        </span>
                      </td>
                      <td class="text-center">
                        <span 
                          :class="['badge', getBudgetStatusClass(budget.status)]"
                        >
                          {{ getBudgetStatusText(budget.status) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="text-center py-4">
              <i class="fas fa-calculator fa-3x text-muted mb-3"></i>
              <p class="text-muted">Детальный бюджетный контроль</p>
              <button @click="generateBudgetReport" class="btn btn-primary">
                <i class="fas fa-file-alt"></i>
                Сформировать бюджетный отчет
              </button>
            </div>
          </div>
        </div>

        <!-- Раздел Аналитические отчеты -->
        <div v-if="activeSection === 'analytics'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-analytics"></i>
              Аналитические отчеты
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3" v-for="report in analyticsReports" :key="report.id">
                <div class="card h-100">
                  <div class="card-body text-center">
                    <i :class="report.icon + ' fa-3x text-primary mb-3'"></i>
                    <h6 class="card-title">{{ report.title }}</h6>
                    <p class="card-text">
                      <small class="text-muted">{{ report.description }}</small>
                    </p>
                    <button 
                      @click="generateAnalyticsReport(report.id)"
                      class="btn btn-outline-primary btn-sm"
                    >
                      <i class="fas fa-chart-bar"></i>
                      Сформировать
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="analyticsReports.length === 0" class="text-center py-4">
              <i class="fas fa-analytics fa-3x text-muted mb-3"></i>
              <p class="text-muted">Аналитические отчеты не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Шаблоны отчетов -->
        <div v-if="activeSection === 'templates'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-file"></i>
              Шаблоны отчетов
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <button 
                @click="createTemplate"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Создать шаблон
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Периодичность</th>
                    <th>Последнее обновление</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="template in templates" :key="template.id">
                    <td>
                      <strong>{{ template.name }}</strong>
                    </td>
                    <td>{{ template.type }}</td>
                    <td>
                      <span class="badge bg-secondary">{{ template.frequency }}</span>
                    </td>
                    <td>
                      <small>{{ formatDate(template.updatedAt) }}</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="useTemplate(template.id)"
                          class="btn btn-outline-primary"
                          title="Использовать шаблон"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                        <button 
                          @click="editTemplate(template.id)"
                          class="btn btn-outline-secondary"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="copyTemplate(template.id)"
                          class="btn btn-outline-success"
                          title="Копировать"
                        >
                          <i class="fas fa-copy"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="templates.length === 0" class="text-center py-4">
              <i class="fas fa-file fa-3x text-muted mb-3"></i>
              <p class="text-muted">Шаблоны отчетов не найдены</p>
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
  name: 'ReportsUZ',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      searchQuery: '',
      contractFilter: 'all',
      
      // Данные дашборда
      dashboardData: {
        totalProcurements: 245,
        totalAmount: 15.7,
        savingsPercent: 12.3,
        activeSuppliers: 89,
        monthlyAmount: 2.1,
        totalContracts: 156
      },

      // Данные закупок
      procurements: [
        {
          id: 1,
          date: new Date('2024-01-15'),
          subject: 'Поставка офисной мебели',
          method: 'Открытый конкурс',
          amount: 2500000,
          savings: 187500,
          status: 'completed'
        },
        {
          id: 2,
          date: new Date('2024-01-20'),
          subject: 'IT-оборудование и программное обеспечение',
          method: 'Электронный аукцион',
          amount: 12000000,
          savings: 960000,
          status: 'in_progress'
        },
        {
          id: 3,
          date: new Date('2024-02-01'),
          subject: 'Услуги по обслуживанию зданий',
          method: 'Запрос котировок',
          amount: 850000,
          savings: 68000,
          status: 'planned'
        }
      ],

      // Данные контрактов
      contracts: [
        {
          id: 1,
          number: 'К-2024-001',
          supplier: 'ООО "ОфисМебельПлюс"',
          subject: 'Поставка офисной мебели',
          amount: 2500000,
          endDate: new Date('2024-12-31'),
          status: 'active'
        },
        {
          id: 2,
          number: 'К-2024-002',
          supplier: 'ООО "ТехноСервис"',
          subject: 'IT-оборудование',
          amount: 12000000,
          endDate: new Date('2024-08-15'),
          status: 'active'
        },
        {
          id: 3,
          number: 'К-2024-003',
          supplier: 'ООО "СервисСтрой"',
          subject: 'Услуги по обслуживанию зданий',
          amount: 850000,
          endDate: new Date('2024-01-10'),
          status: 'expired'
        }
      ],

      // Данные поставщиков
      suppliers: [
        {
          id: 1,
          name: 'ООО "ОфисМебельПлюс"',
          category: 'Мебель и интерьер',
          procurements: 15,
          totalAmount: 35000000,
          rating: 4.5
        },
        {
          id: 2,
          name: 'ООО "ТехноСервис"',
          category: 'IT и коммуникации',
          procurements: 8,
          totalAmount: 185000000,
          rating: 4.8
        },
        {
          id: 3,
          name: 'ООО "СервисСтрой"',
          category: 'Строительные услуги',
          procurements: 12,
          totalAmount: 25000000,
          rating: 4.2
        }
      ],

      // Данные бюджета
      budgetItems: [
        {
          id: 1,
          category: 'IT и оборудование',
          planned: 50000000,
          actual: 48200000,
          deviation: -1800000,
          status: 'under_budget'
        },
        {
          id: 2,
          category: 'Офисные материалы',
          planned: 15000000,
          actual: 16800000,
          deviation: 1800000,
          status: 'over_budget'
        },
        {
          id: 3,
          category: 'Услуги и подрядные работы',
          planned: 25000000,
          actual: 23500000,
          deviation: -1500000,
          status: 'under_budget'
        }
      ],

      // Аналитические отчеты
      analyticsReports: [
        {
          id: 1,
          title: 'Анализ конкурентности закупок',
          description: 'Исследование уровня конкуренции в закупочных процедурах',
          icon: 'fas fa-trophy'
        },
        {
          id: 2,
          title: 'Эффективность процедур',
          description: 'Анализ сроков и качества исполнения закупок',
          icon: 'fas fa-chart-line'
        },
        {
          id: 3,
          title: 'Риски закупочной деятельности',
          description: 'Оценка и мониторинг рисков в сфере закупок',
          icon: 'fas fa-shield-alt'
        },
        {
          id: 4,
          title: 'Динамика экономии средств',
          description: 'Анализ трендов экономии бюджетных средств',
          icon: 'fas fa-piggy-bank'
        },
        {
          id: 5,
          title: 'Анализ поставщиков',
          description: 'Детальный анализ деятельности поставщиков',
          icon: 'fas fa-users'
        },
        {
          id: 6,
          title: 'Сезонность закупок',
          description: 'Выявление сезонных закономерностей в закупках',
          icon: 'fas fa-calendar-alt'
        }
      ],

      // Шаблоны отчетов
      templates: [
        {
          id: 1,
          name: 'Ежемесячный отчет по закупкам',
          type: 'Периодический',
          frequency: 'Месячно',
          updatedAt: new Date('2024-01-15')
        },
        {
          id: 2,
          name: 'Квартальный анализ контрактов',
          type: 'Аналитический',
          frequency: 'Ежеквартально',
          updatedAt: new Date('2024-01-10')
        },
        {
          id: 3,
          name: 'Годовой отчет по поставщикам',
          type: 'Итоговый',
          frequency: 'Ежегодно',
          updatedAt: new Date('2024-01-05')
        }
      ]
    };
  },
  computed: {
    filteredProcurements() {
      if (!this.searchQuery) return this.procurements;
      return this.procurements.filter(procurement => 
        procurement.subject.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    filteredContracts() {
      if (this.contractFilter === 'all') return this.contracts;
      return this.contracts.filter(contract => contract.status === this.contractFilter);
    }
  },
  methods: {
    async refreshData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Имитация обновления данных
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('Отчеты УЗ данные обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    exportData() {
      // Имитация экспорта данных
      console.log('Экспорт данных Отчеты УЗ');
      alert('Экспорт данных Отчеты УЗ (заглушка)');
    },

    generateReport() {
      console.log('Создание отчета');
      alert('Создание отчета (заглушка)');
    },

    exportProcurements() {
      console.log('Экспорт закупок');
      alert('Экспорт закупок (заглушка)');
    },

    viewProcurement(procurementId) {
      console.log(`Просмотр закупки ${procurementId}`);
      alert(`Просмотр закупки ${procurementId} (заглушка)`);
    },

    generateProcurementReport(procurementId) {
      console.log(`Отчет по закупке ${procurementId}`);
      alert(`Отчет по закупке ${procurementId} (заглушка)`);
    },

    createContract() {
      console.log('Создание нового контракта');
      alert('Создание нового контракта (заглушка)');
    },

    viewContract(contractId) {
      console.log(`Просмотр контракта ${contractId}`);
      alert(`Просмотр контракта ${contractId} (заглушка)`);
    },

    generateContractReport(contractId) {
      console.log(`Отчет по контракту ${contractId}`);
      alert(`Отчет по контракту ${contractId} (заглушка)`);
    },

    viewSupplier(supplierId) {
      console.log(`Просмотр поставщика ${supplierId}`);
      alert(`Просмотр поставщика ${supplierId} (заглушка)`);
    },

    generateSupplierReport(supplierId) {
      console.log(`Отчет по поставщику ${supplierId}`);
      alert(`Отчет по поставщику ${supplierId} (заглушка)`);
    },

    generateBudgetReport() {
      console.log('Формирование бюджетного отчета');
      alert('Формирование бюджетного отчета (заглушка)');
    },

    generateAnalyticsReport(reportId) {
      console.log(`Формирование аналитического отчета ${reportId}`);
      alert(`Формирование аналитического отчета ${reportId} (заглушка)`);
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

    copyTemplate(templateId) {
      console.log(`Копирование шаблона ${templateId}`);
      alert(`Копирование шаблона ${templateId} (заглушка)`);
    },

    getProcurementStatusClass(status) {
      const classes = {
        planned: 'bg-info',
        in_progress: 'bg-warning',
        completed: 'bg-success',
        cancelled: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getProcurementStatusText(status) {
      const texts = {
        planned: 'Запланирован',
        in_progress: 'В процессе',
        completed: 'Завершен',
        cancelled: 'Отменен'
      };
      return texts[status] || status;
    },

    getContractStatusClass(status) {
      const classes = {
        active: 'bg-success',
        expired: 'bg-danger',
        pending: 'bg-warning'
      };
      return classes[status] || 'bg-secondary';
    },

    getContractStatusText(status) {
      const texts = {
        active: 'Активный',
        expired: 'Истек',
        pending: 'Ожидает'
      };
      return texts[status] || status;
    },

    getBudgetStatusClass(status) {
      const classes = {
        under_budget: 'bg-success',
        over_budget: 'bg-danger',
        on_budget: 'bg-info'
      };
      return classes[status] || 'bg-secondary';
    },

    getBudgetStatusText(status) {
      const texts = {
        under_budget: 'В пределах бюджета',
        over_budget: 'Превышение бюджета',
        on_budget: 'Точно по бюджету'
      };
      return texts[status] || status;
    },

    formatDate(date) {
      if (!date) return '';
      
      const d = new Date(date);
      return d.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  },
  mounted() {
    console.log('Отчеты УЗ компонента инициализирована');
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

.text-right {
  text-align: right;
}

.progress {
  height: 8px;
}

.card .card-body h4 {
  font-size: 1.5rem;
  font-weight: 700;
}

.opacity-75 {
  opacity: 0.75;
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
  
  .card .card-body h4 {
    font-size: 1.25rem;
  }
}
</style>