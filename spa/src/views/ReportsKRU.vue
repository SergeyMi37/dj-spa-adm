<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-search-dollar"></i> Отчеты КРУ</h2>
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
              Отчеты Контрольно-ревизионного Управления
            </h5>
            <p class="card-text">
              Система контроля и ревизий предназначена для планирования, проведения и мониторинга 
              контрольных мероприятий, выявления нарушений и контроля за их устранением в рамках 
              финансово-хозяйственной деятельности организации.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации КРУ -->
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
              Дашборд КРУ
            </button>
            <button 
              @click="activeSection = 'plans'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'plans' }]"
            >
              <i class="fas fa-calendar-check me-2"></i>
              Планы ревизий
            </button>
            <button 
              @click="activeSection = 'acts'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'acts' }]"
            >
              <i class="fas fa-file-contract me-2"></i>
              Акты ревизий
            </button>
            <button 
              @click="activeSection = 'violations'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'violations' }]"
            >
              <i class="fas fa-exclamation-triangle me-2"></i>
              Нарушения
            </button>
            <button 
              @click="activeSection = 'elimination'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'elimination' }]"
            >
              <i class="fas fa-tools me-2"></i>
              Устранение нарушений
            </button>
            <button 
              @click="activeSection = 'statistics'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'statistics' }]"
            >
              <i class="fas fa-chart-bar me-2"></i>
              Статистика нарушений
            </button>
            <button 
              @click="activeSection = 'documents'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'documents' }]"
            >
              <i class="fas fa-folder-open me-2"></i>
              Документооборот
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Дашборд КРУ -->
        <div v-if="activeSection === 'dashboard'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-line"></i>
              Дашборд Контрольно-ревизионного Управления
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
                        <h4>{{ dashboardData.totalReviews }}</h4>
                        <small>Всего ревизий</small>
                      </div>
                      <i class="fas fa-search fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-warning text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.violationsFound }}</h4>
                        <small>Выявлено нарушений</small>
                      </div>
                      <i class="fas fa-exclamation-triangle fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-success text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.violationsResolved }}</h4>
                        <small>Устранено нарушений</small>
                      </div>
                      <i class="fas fa-check-circle fa-2x opacity-75"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="card bg-info text-white">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h4>{{ dashboardData.reviewEffectiveness }}%</h4>
                        <small>Эффективность ревизий</small>
                      </div>
                      <i class="fas fa-chart-line fa-2x opacity-75"></i>
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
                    <h6 class="mb-0">Динамика проведения ревизий</h6>
                  </div>
                  <div class="card-body">
                    <div class="text-center py-4">
                      <i class="fas fa-chart-bar fa-3x text-muted mb-3"></i>
                      <p class="text-muted">График ревизий по месяцам</p>
                      <small class="text-muted">Запланировано: {{ dashboardData.plannedReviews }} ревизий</small>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-6 mb-3">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">Категории нарушений</h6>
                  </div>
                  <div class="card-body">
                    <div class="text-center py-4">
                      <i class="fas fa-chart-pie fa-3x text-muted mb-3"></i>
                      <p class="text-muted">Распределение по типам</p>
                      <small class="text-muted">Всего типов: {{ dashboardData.violationTypes }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Раздел Планы ревизий -->
        <div v-if="activeSection === 'plans'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-calendar-check"></i>
              Планы ревизий
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по объекту проверки..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group">
                <button 
                  @click="createReviewPlan"
                  class="btn btn-success btn-sm"
                >
                  <i class="fas fa-plus"></i>
                  Создать план
                </button>
                <button 
                  @click="exportReviewPlans"
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
                    <th>Дата создания</th>
                    <th>Объект проверки</th>
                    <th>Тип ревизии</th>
                    <th>Плановая дата</th>
                    <th>Статус</th>
                    <th>Ответственный</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="plan in filteredReviewPlans" :key="plan.id">
                    <td>
                      <small>{{ formatDate(plan.createdDate) }}</small>
                    </td>
                    <td>{{ plan.subject }}</td>
                    <td>
                      <small>{{ plan.reviewType }}</small>
                    </td>
                    <td>
                      <small>{{ formatDate(plan.plannedDate) }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getPlanStatusClass(plan.status)]"
                      >
                        {{ getPlanStatusText(plan.status) }}
                      </span>
                    </td>
                    <td>
                      <small>{{ plan.responsible }}</small>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewReviewPlan(plan.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="editReviewPlan(plan.id)"
                          class="btn btn-outline-secondary"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="generateReviewPlanReport(plan.id)"
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

            <div v-if="filteredReviewPlans.length === 0" class="text-center py-4">
              <i class="fas fa-calendar-check fa-3x text-muted mb-3"></i>
              <p class="text-muted">Планы ревизий не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Акты ревизий -->
        <div v-if="activeSection === 'acts'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-file-contract"></i>
              Акты ревизий
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group" role="group">
                <button 
                  @click="actFilter = 'all'"
                  :class="['btn', 'btn-sm', actFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все акты
                </button>
                <button 
                  @click="actFilter = 'approved'"
                  :class="['btn', 'btn-sm', actFilter === 'approved' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Утвержденные
                </button>
                <button 
                  @click="actFilter = 'pending'"
                  :class="['btn', 'btn-sm', actFilter === 'pending' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  На утверждении
                </button>
                <button 
                  @click="actFilter = 'draft'"
                  :class="['btn', 'btn-sm', actFilter === 'draft' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Черновики
                </button>
              </div>
              <button 
                @click="createReviewAct"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Создать акт
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Номер акта</th>
                    <th>Дата утверждения</th>
                    <th>Объект проверки</th>
                    <th>Выявлено нарушений</th>
                    <th>Сумма ущерба</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="act in filteredReviewActs" :key="act.id">
                    <td>
                      <strong>{{ act.number }}</strong>
                    </td>
                    <td>
                      <small>{{ formatDate(act.approvedDate) }}</small>
                    </td>
                    <td>{{ act.subject }}</td>
                    <td class="text-center">
                      <span class="badge bg-warning">{{ act.violationsCount }}</span>
                    </td>
                    <td class="text-right">
                      <span class="text-danger">
                        {{ act.damageAmount.toLocaleString('ru-RU') }} ₽
                      </span>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getActStatusClass(act.status)]"
                      >
                        {{ getActStatusText(act.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewReviewAct(act.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="generateReviewActReport(act.id)"
                          class="btn btn-outline-success"
                          title="Отчет по акту"
                        >
                          <i class="fas fa-file-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredReviewActs.length === 0" class="text-center py-4">
              <i class="fas fa-file-contract fa-3x text-muted mb-3"></i>
              <p class="text-muted">Акты ревизий не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Нарушения -->
        <div v-if="activeSection === 'violations'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-exclamation-triangle"></i>
              Нарушения
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group" role="group">
                <button 
                  @click="violationFilter = 'all'"
                  :class="['btn', 'btn-sm', violationFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все нарушения
                </button>
                <button 
                  @click="violationFilter = 'serious'"
                  :class="['btn', 'btn-sm', violationFilter === 'serious' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Серьезные
                </button>
                <button 
                  @click="violationFilter = 'moderate'"
                  :class="['btn', 'btn-sm', violationFilter === 'moderate' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Средней тяжести
                </button>
                <button 
                  @click="violationFilter = 'minor'"
                  :class="['btn', 'btn-sm', violationFilter === 'minor' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Незначительные
                </button>
              </div>
              <button 
                @click="createViolation"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Зарегистрировать нарушение
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Дата выявления</th>
                    <th>Описание нарушения</th>
                    <th>Объект</th>
                    <th>Категория</th>
                    <th>Серьезность</th>
                    <th>Статус устранения</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="violation in filteredViolations" :key="violation.id">
                    <td>
                      <small>{{ formatDate(violation.detectionDate) }}</small>
                    </td>
                    <td>
                      <strong>{{ violation.description }}</strong>
                    </td>
                    <td>
                      <small>{{ violation.subject }}</small>
                    </td>
                    <td>
                      <span class="badge bg-secondary">{{ violation.category }}</span>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getViolationSeverityClass(violation.severity)]"
                      >
                        {{ getViolationSeverityText(violation.severity) }}
                      </span>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getViolationStatusClass(violation.status)]"
                      >
                        {{ getViolationStatusText(violation.status) }}
                      </span>
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
                          @click="editViolation(violation.id)"
                          class="btn btn-outline-secondary"
                          title="Редактировать"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="generateViolationReport(violation.id)"
                          class="btn btn-outline-success"
                          title="Отчет по нарушению"
                        >
                          <i class="fas fa-file-alt"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredViolations.length === 0" class="text-center py-4">
              <i class="fas fa-exclamation-triangle fa-3x text-muted mb-3"></i>
              <p class="text-muted">Нарушения не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Устранение нарушений -->
        <div v-if="activeSection === 'elimination'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-tools"></i>
              Устранение нарушений
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-4">
              <h6>Контроль устранения нарушений</h6>
              <div class="table-responsive">
                <table class="table table-hover table-sm">
                  <thead>
                    <tr>
                      <th>Нарушение</th>
                      <th>Ответственный</th>
                      <th>Срок устранения</th>
                      <th>Текущий статус</th>
                      <th>Прогресс</th>
                      <th>Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in eliminationItems" :key="item.id">
                      <td>
                        <strong>{{ item.violation }}</strong>
                      </td>
                      <td>{{ item.responsible }}</td>
                      <td>
                        <small>{{ formatDate(item.dueDate) }}</small>
                      </td>
                      <td>
                        <span 
                          :class="['badge', getEliminationStatusClass(item.status)]"
                        >
                          {{ getEliminationStatusText(item.status) }}
                        </span>
                      </td>
                      <td>
                        <div class="progress" style="height: 6px;">
                          <div 
                            class="progress-bar" 
                            :class="getProgressBarClass(item.progress)"
                            :style="{ width: item.progress + '%' }"
                          ></div>
                        </div>
                        <small class="text-muted">{{ item.progress }}%</small>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button 
                            @click="updateEliminationProgress(item.id)"
                            class="btn btn-outline-primary"
                            title="Обновить прогресс"
                          >
                            <i class="fas fa-edit"></i>
                          </button>
                          <button 
                            @click="markAsResolved(item.id)"
                            class="btn btn-outline-success"
                            title="Отметить как решенное"
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
            <div class="text-center py-4">
              <i class="fas fa-tools fa-3x text-muted mb-3"></i>
              <p class="text-muted">Детальный контроль устранения нарушений</p>
              <button @click="generateEliminationReport" class="btn btn-primary">
                <i class="fas fa-file-alt"></i>
                Сформировать отчет по устранению
              </button>
            </div>
          </div>
        </div>

        <!-- Раздел Статистика нарушений -->
        <div v-if="activeSection === 'statistics'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-chart-bar"></i>
              Статистика нарушений
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3" v-for="stat in violationStatistics" :key="stat.id">
                <div class="card h-100">
                  <div class="card-body text-center">
                    <i :class="stat.icon + ' fa-3x text-primary mb-3'"></i>
                    <h6 class="card-title">{{ stat.title }}</h6>
                    <h4 class="text-primary">{{ stat.value }}</h4>
                    <p class="card-text">
                      <small class="text-muted">{{ stat.description }}</small>
                    </p>
                    <button 
                      @click="generateStatisticsReport(stat.id)"
                      class="btn btn-outline-primary btn-sm"
                    >
                      <i class="fas fa-chart-line"></i>
                      Подробная статистика
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="violationStatistics.length === 0" class="text-center py-4">
              <i class="fas fa-chart-bar fa-3x text-muted mb-3"></i>
              <p class="text-muted">Статистика нарушений не найдена</p>
            </div>
          </div>
        </div>

        <!-- Раздел Документооборот -->
        <div v-if="activeSection === 'documents'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-folder-open"></i>
              Документооборот КРУ
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="documentSearchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по названию документа..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="btn-group">
                <button 
                  @click="uploadDocument"
                  class="btn btn-success btn-sm"
                >
                  <i class="fas fa-upload"></i>
                  Загрузить документ
                </button>
                <button 
                  @click="createDocument"
                  class="btn btn-primary btn-sm"
                >
                  <i class="fas fa-plus"></i>
                  Создать документ
                </button>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Дата создания</th>
                    <th>Автор</th>
                    <th>Размер</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="document in filteredDocuments" :key="document.id">
                    <td>
                      <strong>{{ document.name }}</strong>
                    </td>
                    <td>
                      <span class="badge bg-info">{{ document.type }}</span>
                    </td>
                    <td>
                      <small>{{ formatDate(document.createdAt) }}</small>
                    </td>
                    <td>
                      <small>{{ document.author }}</small>
                    </td>
                    <td>
                      <small>{{ document.size }}</small>
                    </td>
                    <td>
                      <span 
                        :class="['badge', getDocumentStatusClass(document.status)]"
                      >
                        {{ getDocumentStatusText(document.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewDocument(document.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="downloadDocument(document.id)"
                          class="btn btn-outline-success"
                          title="Скачать"
                        >
                          <i class="fas fa-download"></i>
                        </button>
                        <button 
                          @click="editDocument(document.id)"
                          class="btn btn-outline-secondary"
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
            <div v-if="filteredDocuments.length === 0" class="text-center py-4">
              <i class="fas fa-folder-open fa-3x text-muted mb-3"></i>
              <p class="text-muted">Документы не найдены</p>
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
  name: 'ReportsKRU',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'dashboard',
      searchQuery: '',
      documentSearchQuery: '',
      actFilter: 'all',
      violationFilter: 'all',
      
      // Данные дашборда
      dashboardData: {
        totalReviews: 47,
        violationsFound: 23,
        violationsResolved: 18,
        reviewEffectiveness: 87,
        plannedReviews: 8,
        violationTypes: 12
      },

      // Данные планов ревизий
      reviewPlans: [
        {
          id: 1,
          createdDate: new Date('2024-01-15'),
          subject: 'Ревизия финансово-хозяйственной деятельности отдела закупок',
          reviewType: 'Плановая ревизия',
          plannedDate: new Date('2024-02-15'),
          status: 'approved',
          responsible: 'Иванов И.И.'
        },
        {
          id: 2,
          createdDate: new Date('2024-01-20'),
          subject: 'Внеплановая проверка использования бюджетных средств',
          reviewType: 'Внеплановая ревизия',
          plannedDate: new Date('2024-02-01'),
          status: 'in_progress',
          responsible: 'Петров П.П.'
        },
        {
          id: 3,
          createdDate: new Date('2024-01-25'),
          subject: 'Контроль исполнения предыдущих рекомендаций',
          reviewType: 'Контрольная проверка',
          plannedDate: new Date('2024-02-10'),
          status: 'draft',
          responsible: 'Сидоров С.С.'
        }
      ],

      // Данные актов ревизий
      reviewActs: [
        {
          id: 1,
          number: 'Акт-2024-001',
          approvedDate: new Date('2024-01-10'),
          subject: 'Ревизия отдела кадров',
          violationsCount: 5,
          damageAmount: 150000,
          status: 'approved'
        },
        {
          id: 2,
          number: 'Акт-2024-002',
          approvedDate: new Date('2024-01-15'),
          subject: 'Проверка использования материальных ценностей',
          violationsCount: 3,
          damageAmount: 85000,
          status: 'approved'
        },
        {
          id: 3,
          number: 'Акт-2024-003',
          approvedDate: new Date('2024-01-20'),
          subject: 'Контроль соблюдения бюджетного законодательства',
          violationsCount: 8,
          damageAmount: 320000,
          status: 'pending'
        }
      ],

      // Данные нарушений
      violations: [
        {
          id: 1,
          detectionDate: new Date('2024-01-10'),
          description: 'Нарушение порядка ведения бухгалтерского учета',
          subject: 'Отдел бухгалтерии',
          category: 'Бухгалтерский учет',
          severity: 'serious',
          status: 'in_progress'
        },
        {
          id: 2,
          detectionDate: new Date('2024-01-12'),
          description: 'Превышение лимитов расходования средств',
          subject: 'Отдел закупок',
          category: 'Бюджетное законодательство',
          severity: 'moderate',
          status: 'resolved'
        },
        {
          id: 3,
          detectionDate: new Date('2024-01-18'),
          description: 'Нарушение сроков представления отчетности',
          subject: 'Планово-экономический отдел',
          category: 'Отчетность',
          severity: 'minor',
          status: 'pending'
        }
      ],

      // Данные устранения нарушений
      eliminationItems: [
        {
          id: 1,
          violation: 'Нарушение порядка ведения бухгалтерского учета',
          responsible: 'Главный бухгалтер',
          dueDate: new Date('2024-02-15'),
          status: 'in_progress',
          progress: 60
        },
        {
          id: 2,
          violation: 'Превышение лимитов расходования средств',
          responsible: 'Начальник отдела закупок',
          dueDate: new Date('2024-01-31'),
          status: 'resolved',
          progress: 100
        },
        {
          id: 3,
          violation: 'Нарушение сроков представления отчетности',
          responsible: 'Экономист',
          dueDate: new Date('2024-02-05'),
          status: 'pending',
          progress: 25
        }
      ],

      // Статистика нарушений
      violationStatistics: [
        {
          id: 1,
          title: 'Общее количество нарушений',
          value: '23',
          description: 'Выявлено с начала года',
          icon: 'fas fa-exclamation-triangle'
        },
        {
          id: 2,
          title: 'Устраненные нарушения',
          value: '18',
          description: '78% от общего количества',
          icon: 'fas fa-check-circle'
        },
        {
          id: 3,
          title: 'Средний срок устранения',
          value: '12 дн.',
          description: 'От выявления до устранения',
          icon: 'fas fa-clock'
        },
        {
          id: 4,
          title: 'Серьезные нарушения',
          value: '7',
          description: 'Требуют особого внимания',
          icon: 'fas fa-exclamation'
        },
        {
          id: 5,
          title: 'Сумма ущерба',
          value: '2.1 млн ₽',
          description: 'Общий размер выявленного ущерба',
          icon: 'fas fa-ruble-sign'
        },
        {
          id: 6,
          title: 'Коэффициент эффективности',
          value: '87%',
          description: 'Эффективность контрольных мероприятий',
          icon: 'fas fa-chart-line'
        }
      ],

      // Документы
      documents: [
        {
          id: 1,
          name: 'План ревизий на 2024 год',
          type: 'План',
          createdAt: new Date('2024-01-05'),
          author: 'Начальник КРУ',
          size: '245 КБ',
          status: 'active'
        },
        {
          id: 2,
          name: 'Акт ревизии отдела кадров №001',
          type: 'Акт',
          createdAt: new Date('2024-01-10'),
          author: 'Ревизор Иванов И.И.',
          size: '156 КБ',
          status: 'active'
        },
        {
          id: 3,
          name: 'Методические рекомендации по устранению нарушений',
          type: 'Методические материалы',
          createdAt: new Date('2024-01-15'),
          author: 'Методист КРУ',
          size: '89 КБ',
          status: 'active'
        }
      ]
    };
  },
  computed: {
    filteredReviewPlans() {
      if (!this.searchQuery) return this.reviewPlans;
      return this.reviewPlans.filter(plan => 
        plan.subject.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    filteredReviewActs() {
      if (this.actFilter === 'all') return this.reviewActs;
      return this.reviewActs.filter(act => act.status === this.actFilter);
    },

    filteredViolations() {
      if (this.violationFilter === 'all') return this.violations;
      return this.violations.filter(violation => violation.severity === this.violationFilter);
    },

    filteredDocuments() {
      if (!this.documentSearchQuery) return this.documents;
      return this.documents.filter(document => 
        document.name.toLowerCase().includes(this.documentSearchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async refreshData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Имитация обновления данных
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('Отчеты КРУ данные обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    exportData() {
      // Имитация экспорта данных
      console.log('Экспорт данных Отчеты КРУ');
      alert('Экспорт данных Отчеты КРУ (заглушка)');
    },

    createReviewPlan() {
      console.log('Создание плана ревизии');
      alert('Создание плана ревизии (заглушка)');
    },

    exportReviewPlans() {
      console.log('Экспорт планов ревизий');
      alert('Экспорт планов ревизий (заглушка)');
    },

    viewReviewPlan(planId) {
      console.log(`Просмотр плана ревизии ${planId}`);
      alert(`Просмотр плана ревизии ${planId} (заглушка)`);
    },

    editReviewPlan(planId) {
      console.log(`Редактирование плана ревизии ${planId}`);
      alert(`Редактирование плана ревизии ${planId} (заглушка)`);
    },

    generateReviewPlanReport(planId) {
      console.log(`Отчет по плану ревизии ${planId}`);
      alert(`Отчет по плану ревизии ${planId} (заглушка)`);
    },

    createReviewAct() {
      console.log('Создание акта ревизии');
      alert('Создание акта ревизии (заглушка)');
    },

    viewReviewAct(actId) {
      console.log(`Просмотр акта ревизии ${actId}`);
      alert(`Просмотр акта ревизии ${actId} (заглушка)`);
    },

    generateReviewActReport(actId) {
      console.log(`Отчет по акту ревизии ${actId}`);
      alert(`Отчет по акту ревизии ${actId} (заглушка)`);
    },

    createViolation() {
      console.log('Регистрация нарушения');
      alert('Регистрация нарушения (заглушка)');
    },

    viewViolation(violationId) {
      console.log(`Просмотр нарушения ${violationId}`);
      alert(`Просмотр нарушения ${violationId} (заглушка)`);
    },

    editViolation(violationId) {
      console.log(`Редактирование нарушения ${violationId}`);
      alert(`Редактирование нарушения ${violationId} (заглушка)`);
    },

    generateViolationReport(violationId) {
      console.log(`Отчет по нарушению ${violationId}`);
      alert(`Отчет по нарушению ${violationId} (заглушка)`);
    },

    updateEliminationProgress(itemId) {
      console.log(`Обновление прогресса устранения ${itemId}`);
      alert(`Обновление прогресса устранения ${itemId} (заглушка)`);
    },

    markAsResolved(itemId) {
      const item = this.eliminationItems.find(i => i.id === itemId);
      if (item) {
        item.status = 'resolved';
        item.progress = 100;
      }
      console.log(`Нарушение ${itemId} отмечено как решенное`);
    },

    generateEliminationReport() {
      console.log('Формирование отчета по устранению нарушений');
      alert('Формирование отчета по устранению нарушений (заглушка)');
    },

    generateStatisticsReport(statId) {
      console.log(`Формирование статистического отчета ${statId}`);
      alert(`Формирование статистического отчета ${statId} (заглушка)`);
    },

    uploadDocument() {
      console.log('Загрузка документа');
      alert('Загрузка документа (заглушка)');
    },

    createDocument() {
      console.log('Создание документа');
      alert('Создание документа (заглушка)');
    },

    viewDocument(documentId) {
      console.log(`Просмотр документа ${documentId}`);
      alert(`Просмотр документа ${documentId} (заглушка)`);
    },

    downloadDocument(documentId) {
      console.log(`Скачивание документа ${documentId}`);
      alert(`Скачивание документа ${documentId} (заглушка)`);
    },

    editDocument(documentId) {
      console.log(`Редактирование документа ${documentId}`);
      alert(`Редактирование документа ${documentId} (заглушка)`);
    },

    getPlanStatusClass(status) {
      const classes = {
        draft: 'bg-secondary',
        approved: 'bg-success',
        in_progress: 'bg-info',
        completed: 'bg-primary',
        cancelled: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getPlanStatusText(status) {
      const texts = {
        draft: 'Черновик',
        approved: 'Утвержден',
        in_progress: 'В процессе',
        completed: 'Завершен',
        cancelled: 'Отменен'
      };
      return texts[status] || status;
    },

    getActStatusClass(status) {
      const classes = {
        draft: 'bg-secondary',
        pending: 'bg-warning',
        approved: 'bg-success',
        rejected: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getActStatusText(status) {
      const texts = {
        draft: 'Черновик',
        pending: 'На утверждении',
        approved: 'Утвержден',
        rejected: 'Отклонен'
      };
      return texts[status] || status;
    },

    getViolationSeverityClass(severity) {
      const classes = {
        minor: 'bg-info',
        moderate: 'bg-warning',
        serious: 'bg-danger'
      };
      return classes[severity] || 'bg-secondary';
    },

    getViolationSeverityText(severity) {
      const texts = {
        minor: 'Незначительное',
        moderate: 'Средней тяжести',
        serious: 'Серьезное'
      };
      return texts[severity] || severity;
    },

    getViolationStatusClass(status) {
      const classes = {
        pending: 'bg-warning',
        in_progress: 'bg-info',
        resolved: 'bg-success',
        closed: 'bg-secondary'
      };
      return classes[status] || 'bg-secondary';
    },

    getViolationStatusText(status) {
      const texts = {
        pending: 'Ожидает рассмотрения',
        in_progress: 'В процессе устранения',
        resolved: 'Устранено',
        closed: 'Закрыто'
      };
      return texts[status] || status;
    },

    getEliminationStatusClass(status) {
      const classes = {
        pending: 'bg-warning',
        in_progress: 'bg-info',
        resolved: 'bg-success',
        overdue: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getEliminationStatusText(status) {
      const texts = {
        pending: 'Ожидает начала',
        in_progress: 'В процессе',
        resolved: 'Решено',
        overdue: 'Просрочено'
      };
      return texts[status] || status;
    },

    getProgressBarClass(progress) {
      if (progress >= 80) return 'bg-success';
      if (progress >= 50) return 'bg-warning';
      return 'bg-danger';
    },

    getDocumentStatusClass(status) {
      const classes = {
        active: 'bg-success',
        archived: 'bg-secondary',
        deleted: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getDocumentStatusText(status) {
      const texts = {
        active: 'Активный',
        archived: 'Архивный',
        deleted: 'Удален'
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
    console.log('Отчеты КРУ компонента инициализирована');
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