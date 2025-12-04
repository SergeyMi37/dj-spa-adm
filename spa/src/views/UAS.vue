<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-chart-pie"></i> УАС ЕАИСТ</h2>
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
              @click="exportAnalysis" 
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
              Универсальный Аналитический Сервис ЕАИСТ
            </h5>
            <p class="card-text">
              УАС ЕАИСТ предоставляет возможности для получения, анализа и визуализации данных 
              из Единой автоматизированной информационной системы торгов. Сервис обеспечивает 
              доступ к аналитическим отчетам, статистике закупок, мониторингу рынка и другим 
              аналитическим функциям для принятия обоснованных решений.
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
                <h3 class="mb-0">{{ keyMetrics.totalTrades }}</h3>
                <p class="mb-0">Всего торгов</p>
              </div>
              <i class="fas fa-gavel fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.totalVolume }} млрд ₽</h3>
                <p class="mb-0">Объем торгов</p>
              </div>
              <i class="fas fa-money-bill-wave fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.activeSuppliers }}</h3>
                <p class="mb-0">Поставщиков</p>
              </div>
              <i class="fas fa-users fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h3 class="mb-0">{{ keyMetrics.avgSavings }}%</h3>
                <p class="mb-0">Средняя экономия</p>
              </div>
              <i class="fas fa-chart-line fa-2x"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации УАС ЕАИСТ -->
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
              Общий анализ
            </button>
            <button 
              @click="activeSection = 'trades'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'trades' }]"
            >
              <i class="fas fa-gavel me-2"></i>
              Анализ торгов
            </button>
            <button 
              @click="activeSection = 'suppliers'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'suppliers' }]"
            >
              <i class="fas fa-users me-2"></i>
              Поставщики
            </button>
            <button 
              @click="activeSection = 'market'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'market' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Анализ рынка
            </button>
            <button 
              @click="activeSection = 'reports'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'reports' }]"
            >
              <i class="fas fa-file-alt me-2"></i>
              Отчеты
            </button>
            <button 
              @click="activeSection = 'queries'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'queries' }]"
            >
              <i class="fas fa-search me-2"></i>
              Аналитические запросы
            </button>
            <button 
              @click="activeSection = 'monitoring'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'monitoring' }]"
            >
              <i class="fas fa-tachometer-alt me-2"></i>
              Мониторинг
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Общий анализ -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-pie"></i>
              Общий анализ ЕАИСТ
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Динамика торгов (12 месяцев)</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="tradesChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Распределение по способам определения поставщика</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="method in procurementMethods" :key="method.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ method.name }}</span>
                        <span class="badge bg-secondary">{{ method.count }}</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :class="method.color"
                          :style="`width: ${(method.count / keyMetrics.totalTrades) * 100}%`"
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
                    <h6>Последние обновления данных</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="update in recentUpdates" :key="update.id" class="d-flex align-items-center mb-2">
                      <i :class="getUpdateIcon(update.type)" class="me-3"></i>
                      <div class="flex-grow-1">
                        <div class="d-flex justify-content-between">
                          <span>{{ update.message }}</span>
                          <small class="text-muted">{{ formatTime(update.timestamp) }}</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Анализ торгов -->
        <div v-if="activeSection === 'trades'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-gavel"></i>
              Анализ торгов
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по номеру или предмету..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group btn-group-sm">
                <button 
                  @click="tradeFilter = 'all'"
                  :class="['btn', tradeFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="tradeFilter = 'completed'"
                  :class="['btn', tradeFilter === 'completed' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Завершенные
                </button>
                <button 
                  @click="tradeFilter = 'cancelled'"
                  :class="['btn', tradeFilter === 'cancelled' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Отмененные
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Номер</th>
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
                  <tr v-for="trade in filteredTrades" :key="trade.id">
                    <td><strong>#{{ trade.id }}</strong></td>
                    <td>
                      <small>{{ formatDate(trade.date) }}</small>
                    </td>
                    <td>
                      <strong>{{ trade.subject }}</strong>
                      <br>
                      <small class="text-muted">{{ trade.customer }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="getMethodBadgeClass(trade.method)">
                        {{ getMethodText(trade.method) }}
                      </span>
                    </td>
                    <td>
                      <strong>{{ trade.amount.toLocaleString('ru-RU') }} ₽</strong>
                    </td>
                    <td>
                      <span 
                        :class="['badge', trade.savings > 0 ? 'bg-success' : 'bg-secondary']"
                      >
                        {{ trade.savings > 0 ? '+' : '' }}{{ trade.savings }}%
                      </span>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getStatusBadgeClass(trade.status)]"
                      >
                        {{ getStatusText(trade.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewTrade(trade.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="analyzeTrade(trade.id)"
                          class="btn btn-outline-info"
                          title="Анализ"
                        >
                          <i class="fas fa-chart-line"></i>
                        </button>
                        <button 
                          @click="exportTrade(trade.id)"
                          class="btn btn-outline-success"
                          title="Экспорт"
                        >
                          <i class="fas fa-download"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredTrades.length === 0" class="text-center py-4">
              <i class="fas fa-gavel fa-3x text-muted mb-3"></i>
              <p class="text-muted">Торги не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Поставщики -->
        <div v-if="activeSection === 'suppliers'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-users"></i>
              Анализ поставщиков
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="supplier in topSuppliers" :key="supplier.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i class="fas fa-building text-primary me-2"></i>
                      {{ supplier.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ supplier.address }}</small>
                    </p>
                    <div class="row text-center">
                      <div class="col-4">
                        <strong>{{ supplier.contracts }}</strong>
                        <br>
                        <small class="text-muted">Контрактов</small>
                      </div>
                      <div class="col-4">
                        <strong>{{ supplier.volume.toLocaleString('ru-RU') }} млн ₽</strong>
                        <br>
                        <small class="text-muted">Объем</small>
                      </div>
                      <div class="col-4">
                        <strong>{{ supplier.rating }}</strong>
                        <br>
                        <small class="text-muted">Рейтинг</small>
                      </div>
                    </div>
                    <div class="mt-2">
                      <button 
                        @click="viewSupplier(supplier.id)"
                        class="btn btn-outline-primary btn-sm btn-block"
                      >
                        Подробнее
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="topSuppliers.length === 0" class="text-center py-4">
              <i class="fas fa-users fa-3x text-muted mb-3"></i>
              <p class="text-muted">Поставщики не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Анализ рынка -->
        <div v-if="activeSection === 'market'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Анализ рынка
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Ценовая аналитика по категориям</h6>
                  </div>
                  <div class="card-body">
                    <canvas id="priceChart" height="200"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Концентрация рынка</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="segment in marketSegments" :key="segment.name" class="mb-2">
                      <div class="d-flex justify-content-between">
                        <span>{{ segment.name }}</span>
                        <span class="badge bg-info">{{ segment.share }}%</span>
                      </div>
                      <div class="progress" style="height: 5px;">
                        <div 
                          class="progress-bar" 
                          :style="`width: ${segment.share}%`"
                        ></div>
                      </div>
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
              <i class="fas fa-file-alt"></i>
              Аналитические отчеты
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <div class="card">
                  <div class="card-header">
                    <h6>Параметры отчета</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <label class="form-label">Период:</label>
                      <select v-model="reportSettings.period" class="form-control form-control-sm">
                        <option value="month">Месяц</option>
                        <option value="quarter">Квартал</option>
                        <option value="year">Год</option>
                      </select>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Тип отчета:</label>
                      <select v-model="reportSettings.type" class="form-control form-control-sm">
                        <option value="summary">Сводный</option>
                        <option value="trades">По торгам</option>
                        <option value="suppliers">По поставщикам</option>
                      </select>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Формат:</label>
                      <select v-model="reportSettings.format" class="form-control form-control-sm">
                        <option value="pdf">PDF</option>
                        <option value="excel">Excel</option>
                        <option value="pptx">PowerPoint</option>
                      </select>
                    </div>
                    <button 
                      @click="generateReport"
                      class="btn btn-primary btn-block"
                    >
                      <i class="fas fa-file-alt me-2"></i>
                      Сформировать отчет
                    </button>
                  </div>
                </div>
              </div>
              <div class="col-md-8">
                <div class="card">
                  <div class="card-header">
                    <h6>Шаблоны отчетов</h6>
                  </div>
                  <div class="card-body">
                    <div class="list-group">
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Исполнительная сводка</h6>
                          <small class="text-muted">Общий анализ деятельности за период</small>
                        </div>
                        <button 
                          @click="useTemplate('executive')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                      </div>
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Анализ эффективности</h6>
                          <small class="text-muted">Оценка эффективности закупочной деятельности</small>
                        </div>
                        <button 
                          @click="useTemplate('efficiency')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                      </div>
                      <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Рыночная аналитика</h6>
                          <small class="text-muted">Анализ конъюнктуры рынка</small>
                        </div>
                        <button 
                          @click="useTemplate('market')"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Аналитические запросы -->
        <div v-if="activeSection === 'queries'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-search"></i>
              Аналитические запросы к ЕАИСТ
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <div class="row">
                <div class="col-md-8">
                  <div class="form-group">
                    <label class="form-label">Запрос к ЕАИСТ:</label>
                    <textarea 
                      v-model="currentQuery"
                      class="form-control" 
                      rows="3" 
                      placeholder="Введите аналитический запрос к данным ЕАИСТ..."
                    ></textarea>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label class="form-label">Шаблоны запросов:</label>
                    <select v-model="queryTemplate" class="form-control form-control-sm">
                      <option value="">Выберите шаблон...</option>
                      <option value="volume_by_month">Объем закупок по месяцам</option>
                      <option value="top_suppliers">Топ-10 поставщиков</option>
                      <option value="price_trends">Динамика цен</option>
                      <option value="competition_analysis">Анализ конкуренции</option>
                    </select>
                    <button 
                      @click="executeQuery"
                      :disabled="!currentQuery.trim() || loading"
                      class="btn btn-primary btn-block mt-2"
                    >
                      <i class="fas fa-play me-2"></i>
                      Выполнить запрос
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="queryResults.length > 0" class="mt-3">
              <div class="card">
                <div class="card-header">
                  <h6>Результаты запроса</h6>
                </div>
                <div class="card-body">
                  <div class="table-responsive">
                    <table class="table table-striped table-sm">
                      <thead>
                        <tr>
                          <th v-for="column in queryColumns" :key="column">{{ column }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, index) in queryResults" :key="index">
                          <td v-for="value in row" :key="value">{{ value }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="queryHistory.length > 0" class="mt-3">
              <h6>История запросов</h6>
              <div class="list-group">
                <div 
                  v-for="query in queryHistory" 
                  :key="query.id" 
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <strong>{{ query.title }}</strong>
                    <br>
                    <small class="text-muted">{{ formatDateTime(query.executed_at) }}</small>
                  </div>
                  <button 
                    @click="rerunQuery(query.id)"
                    class="btn btn-outline-secondary btn-sm"
                  >
                    <i class="fas fa-redo"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Мониторинг -->
        <div v-if="activeSection === 'monitoring'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-tachometer-alt"></i>
              Мониторинг ЕАИСТ
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Статус интеграции</h6>
                  </div>
                  <div class="card-body">
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Соединение с ЕАИСТ:</span>
                        <span 
                          :class="integrationStatus.connected ? 'text-success' : 'text-danger'"
                          class="fw-bold"
                        >
                          {{ integrationStatus.connected ? 'Подключено' : 'Отключено' }}
                        </span>
                      </div>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Последняя синхронизация:</span>
                        <small>{{ formatDateTime(integrationStatus.lastSync) }}</small>
                      </div>
                    </div>
                    <div class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>Время ответа:</span>
                        <span>{{ integrationStatus.responseTime }} мс</span>
                      </div>
                    </div>
                    <div class="progress mb-2">
                      <div 
                        class="progress-bar bg-success" 
                        role="progressbar" 
                        :style="`width: ${integrationStatus.health}%`"
                      >
                        {{ integrationStatus.health }}%
                      </div>
                    </div>
                    <small class="text-muted">Здоровье системы</small>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6>Мониторинг обновлений</h6>
                  </div>
                  <div class="card-body">
                    <div v-for="metric in monitoringMetrics" :key="metric.name" class="mb-3">
                      <div class="d-flex justify-content-between">
                        <span>{{ metric.name }}</span>
                        <span class="badge" :class="metric.status === 'good' ? 'bg-success' : 'bg-warning'">
                          {{ metric.value }}
                        </span>
                      </div>
                      <small class="text-muted">{{ metric.description }}</small>
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
  name: 'UAS',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      searchQuery: '',
      tradeFilter: 'all',
      
      // Ключевые показатели
      keyMetrics: {
        totalTrades: 89456,
        totalVolume: 125.7,
        activeSuppliers: 2341,
        avgSavings: 12.3
      },

      // Методы закупок
      procurementMethods: [
        { name: 'Конкурс с ограниченным участием', count: 2456, color: 'bg-primary' },
        { name: 'Аукцион в электронной форме', count: 1892, color: 'bg-success' },
        { name: 'Запрос котировок', count: 1234, color: 'bg-warning' },
        { name: 'Запрос предложений', count: 892, color: 'bg-info' },
        { name: 'Закупка у единственного поставщика', count: 567, color: 'bg-danger' }
      ],

      // Последние обновления
      recentUpdates: [
        {
          id: 1,
          type: 'data_updated',
          message: 'Обновлены данные по торгам за текущий месяц',
          timestamp: new Date('2024-01-15T10:30:00')
        },
        {
          id: 2,
          type: 'report_generated',
          message: 'Сформирован отчет по эффективности закупок',
          timestamp: new Date('2024-01-15T09:15:00')
        },
        {
          id: 3,
          type: 'integration_restored',
          message: 'Восстановлено соединение с ЕАИСТ',
          timestamp: new Date('2024-01-15T08:45:00')
        }
      ],

      // Торги
      trades: [
        {
          id: 'EAI001',
          date: new Date('2024-01-15'),
          subject: 'Поставка медицинского оборудования',
          customer: 'ГБУЗ "Городская больница №1"',
          method: 'auction',
          amount: 15000000,
          savings: 15.2,
          status: 'completed'
        },
        {
          id: 'EAI002',
          date: new Date('2024-01-14'),
          subject: 'Капитальный ремонт здания',
          customer: 'МБОУ "Средняя школа №10"',
          method: 'contest',
          amount: 8500000,
          savings: 8.7,
          status: 'completed'
        },
        {
          id: 'EAI003',
          date: new Date('2024-01-13'),
          subject: 'Поставка канцелярских товаров',
          customer: 'Администрация города',
          method: 'quotation',
          amount: 450000,
          savings: 12.1,
          status: 'cancelled'
        }
      ],

      // Топ поставщики
      topSuppliers: [
        {
          id: 1,
          name: 'ООО "МедТехПлюс"',
          address: 'г. Москва, ул. Медицинская, д. 15',
          contracts: 156,
          volume: 45.7,
          rating: 4.8
        },
        {
          id: 2,
          name: 'АО "СтройМатериалы"',
          address: 'г. Санкт-Петербург, пр. Строителей, д. 25',
          contracts: 134,
          volume: 38.2,
          rating: 4.6
        },
        {
          id: 3,
          name: 'ИП Иванов И.И.',
          address: 'г. Екатеринбург, ул. Торговая, д. 8',
          contracts: 89,
          volume: 23.1,
          rating: 4.9
        }
      ],

      // Сегменты рынка
      marketSegments: [
        { name: 'Медицинские товары', share: 32 },
        { name: 'Строительные материалы', share: 28 },
        { name: 'IT оборудование', share: 18 },
        { name: 'Транспортные услуги', share: 12 },
        { name: 'Прочие услуги', share: 10 }
      ],

      // Настройки отчетов
      reportSettings: {
        period: 'month',
        type: 'summary',
        format: 'pdf'
      },

      // Аналитические запросы
      currentQuery: '',
      queryTemplate: '',
      queryResults: [],
      queryColumns: [],
      queryHistory: [
        {
          id: 1,
          title: 'Объем закупок за квартал',
          query: 'SELECT month, SUM(amount) FROM trades WHERE quarter = Q4 GROUP BY month',
          executed_at: new Date('2024-01-15T10:00:00')
        }
      ],

      // Статус интеграции
      integrationStatus: {
        connected: true,
        lastSync: new Date('2024-01-15T10:30:00'),
        responseTime: 1250,
        health: 95
      },

      // Мониторинг метрики
      monitoringMetrics: [
        { 
          name: 'Свежесть данных', 
          value: '2 часа', 
          status: 'good', 
          description: 'Время с последнего обновления данных' 
        },
        { 
          name: 'Покрытие источников', 
          value: '98%', 
          status: 'good', 
          description: 'Процент доступных источников данных' 
        },
        { 
          name: 'Качество данных', 
          value: 'Хорошее', 
          status: 'good', 
          description: 'Оценка качества загруженных данных' 
        }
      ]
    };
  },
  computed: {
    filteredTrades() {
      let filtered = this.trades;
      
      if (this.searchQuery) {
        filtered = filtered.filter(trade => 
          trade.subject.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          trade.id.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          trade.customer.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
      if (this.tradeFilter !== 'all') {
        filtered = filtered.filter(trade => trade.status === this.tradeFilter);
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
        console.log('Данные УАС ЕАИСТ обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    exportAnalysis() {
      console.log('Экспорт анализа УАС ЕАИСТ');
      alert('Экспорт анализа УАС ЕАИСТ (заглушка)');
    },

    viewTrade(tradeId) {
      console.log(`Просмотр торгов ${tradeId}`);
      alert(`Просмотр торгов ${tradeId} (заглушка)`);
    },

    analyzeTrade(tradeId) {
      console.log(`Анализ торгов ${tradeId}`);
      alert(`Анализ торгов ${tradeId} (заглушка)`);
    },

    exportTrade(tradeId) {
      console.log(`Экспорт торгов ${tradeId}`);
      alert(`Экспорт торгов ${tradeId} (заглушка)`);
    },

    viewSupplier(supplierId) {
      console.log(`Просмотр поставщика ${supplierId}`);
      alert(`Просмотр поставщика ${supplierId} (заглушка)`);
    },

    generateReport() {
      console.log('Генерация отчета УАС ЕАИСТ');
      alert(`Генерация отчета типа "${this.reportSettings.type}" (заглушка)`);
    },

    useTemplate(templateType) {
      console.log(`Использование шаблона: ${templateType}`);
      alert(`Использование шаблона "${templateType}" (заглушка)`);
    },

    executeQuery() {
      if (!this.currentQuery.trim()) return;
      
      this.loading = true;
      setTimeout(() => {
        // Имитация выполнения запроса
        this.queryResults = [
          ['Январь', '45.2 млн ₽', '234 торгов'],
          ['Февраль', '52.1 млн ₽', '267 торгов'],
          ['Март', '48.7 млн ₽', '245 торгов']
        ];
        this.queryColumns = ['Месяц', 'Объем', 'Количество торгов'];
        
        // Добавляем в историю
        this.queryHistory.unshift({
          id: Date.now(),
          title: `Запрос от ${new Date().toLocaleDateString()}`,
          query: this.currentQuery,
          executed_at: new Date()
        });
        
        this.loading = false;
      }, 2000);
    },

    rerunQuery(queryId) {
      const query = this.queryHistory.find(q => q.id === queryId);
      if (query) {
        this.currentQuery = query.query;
        this.executeQuery();
      }
    },

    // Вспомогательные методы
    getUpdateIcon(type) {
      const icons = {
        data_updated: 'fas fa-sync text-primary',
        report_generated: 'fas fa-file-alt text-success',
        integration_restored: 'fas fa-plug text-info'
      };
      return icons[type] || 'fas fa-info-circle text-secondary';
    },

    getMethodBadgeClass(method) {
      const classes = {
        auction: 'bg-primary',
        contest: 'bg-success',
        quotation: 'bg-warning',
        proposal: 'bg-info',
        single: 'bg-secondary'
      };
      return classes[method] || 'bg-secondary';
    },

    getMethodText(method) {
      const texts = {
        auction: 'Аукцион',
        contest: 'Конкурс',
        quotation: 'Котировки',
        proposal: 'Предложения',
        single: 'Единственный'
      };
      return texts[method] || method;
    },

    getStatusBadgeClass(status) {
      const classes = {
        completed: 'bg-success',
        cancelled: 'bg-danger',
        pending: 'bg-warning'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusText(status) {
      const texts = {
        completed: 'Завершена',
        cancelled: 'Отменена',
        pending: 'В процессе'
      };
      return texts[status] || status;
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
  watch: {
    queryTemplate(newTemplate) {
      if (newTemplate) {
        const templates = {
          volume_by_month: 'SELECT month, SUM(amount) as total_volume FROM trades GROUP BY month ORDER BY month',
          top_suppliers: 'SELECT name, COUNT(*) as contracts, SUM(amount) as total_volume FROM suppliers JOIN contracts ON suppliers.id = contracts.supplier_id GROUP BY name ORDER BY total_volume DESC LIMIT 10',
          price_trends: 'SELECT product_category, AVG(price) as avg_price, DATE_FORMAT(date, "%Y-%m") as month FROM prices GROUP BY product_category, month ORDER BY month',
          competition_analysis: 'SELECT COUNT(DISTINCT supplier_id) as competitors, AVG(final_price/original_price) as avg_discount FROM contracts GROUP BY product_category'
        };
        this.currentQuery = templates[newTemplate] || '';
      }
    }
  },
  mounted() {
    console.log('Компонента УАС ЕАИСТ инициализирована');
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