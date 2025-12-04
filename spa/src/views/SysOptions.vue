<template>
  <div class="row">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Системные опции</h3>
          <div class="card-tools">
            <button @click="loadSysOptions" class="btn btn-primary btn-sm" :disabled="loading">
              <i class="fas fa-sync"></i>
              {{ loading ? 'Загрузка...' : 'Обновить' }}
            </button>
            <button @click="showFontAwesomeModal" class="btn btn-success btn-sm ml-2">
              <i class="fas fa-icons"></i>
              Font Awesome Icons
            </button>
          </div>
        </div>
        <div class="card-body">
          <!-- Пагинатор -->
          <div class="d-flex justify-content-between align-items-center mb-3 p-2 border rounded bg-light">
            <div class="d-flex align-items-center">
              <label for="limit" class="form-label me-2 mb-0">Записей на странице:</label>
              <select id="limit" v-model="limit" class="form-control" style="width: auto; display: inline-block;" @change="onLimitChange">
                <option value="5">5</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="1000">1000</option>
              </select>
            </div>
            
            <div v-if="pagination.total_pages > 1" class="d-flex align-items-center">
              <button
                @click="goToFirstPage"
                class="btn btn-outline-secondary btn-sm me-1"
                :disabled="pagination.current_page === 1 || loading"
                title="В начало"
              >
                « В начало
              </button>
              <button
                @click="changePage(pagination.current_page - 1)"
                class="btn btn-outline-primary btn-sm me-2"
                :disabled="!pagination.has_previous || loading"
              >
                « Предыдущая
              </button>
              <span class="badge badge-info me-2">
                Страница {{ pagination.current_page }} из {{ pagination.total_pages }}
              </span>
              <button
                @click="changePage(pagination.current_page + 1)"
                class="btn btn-outline-primary btn-sm me-2"
                :disabled="!pagination.has_next || loading"
              >
                Следующая »
              </button>
              <button
                @click="goToLastPage"
                class="btn btn-outline-secondary btn-sm"
                :disabled="pagination.current_page === pagination.total_pages || loading"
                title="В конец"
              >
                В конец »
              </button>
            </div>
          </div>

          <!-- Информация о пагинации -->
          <div v-if="pagination.total_count" class="mb-2">
            <small class="text-muted">
              Всего записей: {{ pagination.total_count }} |
              На странице: {{ pagination.limit }} |
              Смещение: {{ pagination.offset }}
            </small>
          </div>

          <div v-if="sysOptions.length > 0" class="table-responsive">
            <table class="table table-striped table-hover">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Название</th>
                  <th>Категория</th>
                  <th>Описание</th>
                  <th>Опции</th>
                  <th>JSON</th>
                  <th>Публичный</th>
                  <th>Пользователь</th>
                  <th>Права доступа</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="option in sysOptions" :key="option.id">
                  <td>{{ option.id }}</td>
                  <td><strong>{{ option.name }}</strong></td>
                  <td>
                    <span class="badge badge-info">{{ option.category }}</span>
                  </td>
                  <td>{{ option.desc || '-' }}</td>
                  <td>{{ option.option || '-' }}</td>
                  <td>
                    <code v-if="option.json" class="text-muted small">{{ option.json }}</code>
                    <span v-else>-</span>
                  </td>
                  <td>
                    <span class="badge" :class="option.public ? 'badge-success' : 'badge-secondary'">
                      <i :class="option.public ? 'fas fa-check' : 'fas fa-times'"></i>
                      {{ option.public ? 'Да' : 'Нет' }}
                    </span>
                  </td>
                  <td>{{ option.user ? option.user.username : 'Система' }}</td>
                  <td>
                    <span v-if="canEditSysOption(option)" class="badge badge-success">
                      <i class="fas fa-edit"></i> Редактирование
                    </span>
                    <span v-else class="badge badge-secondary">
                      <i class="fas fa-eye"></i> Только чтение
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else-if="!loading" class="text-center text-muted">
            <i class="fas fa-cogs fa-3x mb-3"></i>
            <p>Нажмите "Обновить" для загрузки системных опций</p>
          </div>

          <div v-if="error" class="alert alert-danger mt-3">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Ошибка:</strong> {{ error }}
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с иконками Font Awesome -->
    <div class="modal fade" id="fontAwesomeModal" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-icons"></i>
              Font Awesome Icons
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <!-- Поиск и фильтры -->
            <div class="row mb-3">
              <div class="col-md-6">
                <input
                  v-model="iconSearchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Поиск иконок..."
                  @input="filterIcons"
                >
              </div>
              <div class="col-md-3">
                <select v-model="selectedStyle" class="form-control" @change="filterIcons">
                  <option value="all">Все стили</option>
                  <option value="fas">Solid (fas)</option>
                  <option value="far">Regular (far)</option>
                  <option value="fab">Brands (fab)</option>
                </select>
              </div>
              <div class="col-md-3">
                <select v-model="selectedCategory" class="form-control" @change="filterIcons">
                  <option value="all">Все категории</option>
                  <option value="interface">Интерфейс</option>
                  <option value="navigation">Навигация</option>
                  <option value="media">Медиа</option>
                  <option value="forms">Формы</option>
                  <option value="arrows">Стрелки</option>
                  <option value="objects">Объекты</option>
                  <option value="text">Текст</option>
                  <option value="transportation">Транспорт</option>
                  <option value="gender">Гендер</option>
                  <option value="payment">Платежи</option>
                  <option value="charts">Диаграммы</option>
                  <option value="currency">Валюта</option>
                  <option value="time">Время</option>
                  <option value="medical">Медицина</option>
                  <option value="accessibility">Доступность</option>
                  <option value="other">Прочие</option>
                </select>
              </div>
            </div>

            <!-- Цветовые схемы -->
            <div class="mb-3">
              <h6>Цветовые схемы:</h6>
              <div class="btn-group btn-group-sm" role="group">
                <button
                  @click="selectedColorScheme = 'default'"
                  :class="['btn', selectedColorScheme === 'default' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Стандарт
                </button>
                <button
                  @click="selectedColorScheme = 'primary'"
                  :class="['btn', selectedColorScheme === 'primary' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Синий
                </button>
                <button
                  @click="selectedColorScheme = 'success'"
                  :class="['btn', selectedColorScheme === 'success' ? 'btn-success' : 'btn-outline-success']"
                >
                  Зеленый
                </button>
                <button
                  @click="selectedColorScheme = 'warning'"
                  :class="['btn', selectedColorScheme === 'warning' ? 'btn-warning' : 'btn-outline-warning']"
                >
                  Оранжевый
                </button>
                <button
                  @click="selectedColorScheme = 'danger'"
                  :class="['btn', selectedColorScheme === 'danger' ? 'btn-danger' : 'btn-outline-danger']"
                >
                  Красный
                </button>
                <button
                  @click="selectedColorScheme = 'info'"
                  :class="['btn', selectedColorScheme === 'info' ? 'btn-info' : 'btn-outline-info']"
                >
                  Голубой
                </button>
              </div>
            </div>

            <!-- Размеры иконок -->
            <div class="mb-3">
              <h6>Размеры:</h6>
              <div class="btn-group btn-group-sm" role="group">
                <button
                  @click="selectedSize = 'xs'"
                  :class="['btn', selectedSize === 'xs' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  xs (0.75em)
                </button>
                <button
                  @click="selectedSize = 'sm'"
                  :class="['btn', selectedSize === 'sm' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  sm (0.875em)
                </button>
                <button
                  @click="selectedSize = 'base'"
                  :class="['btn', selectedSize === 'base' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  base (1em)
                </button>
                <button
                  @click="selectedSize = 'lg'"
                  :class="['btn', selectedSize === 'lg' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  lg (1.33em)
                </button>
                <button
                  @click="selectedSize = '2x'"
                  :class="['btn', selectedSize === '2x' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  2x (2em)
                </button>
                <button
                  @click="selectedSize = '3x'"
                  :class="['btn', selectedSize === '3x' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  3x (3em)
                </button>
                <button
                  @click="selectedSize = '5x'"
                  :class="['btn', selectedSize === '5x' ? 'btn-secondary' : 'btn-outline-secondary']"
                >
                  5x (5em)
                </button>
              </div>
            </div>

            <!-- Счетчик найденных иконок -->
            <div class="mb-2">
              <small class="text-muted">
                Найдено иконок: {{ filteredIcons.length }} из {{ fontAwesomeIcons.length }}
              </small>
            </div>

            <!-- Сетка иконок -->
            <div class="row" style="max-height: 400px; overflow-y: auto;">
              <div
                v-for="icon in filteredIcons"
                :key="icon.name"
                class="col-lg-2 col-md-3 col-sm-4 col-6 mb-3"
              >
                <div
                  class="text-center p-3 border rounded cursor-pointer hover-effect"
                  @click="copyIconCode(icon)"
                  :title="icon.name"
                >
                  <div :class="getIconClasses(icon)">
                    <i :class="icon.className"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-muted d-block">{{ icon.name }}</small>
                    <small class="text-info">{{ icon.style }} {{ icon.category }}</small>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="filteredIcons.length === 0" class="text-center py-4">
              <i class="fas fa-search fa-3x text-muted mb-3"></i>
              <p class="text-muted">Иконки не найдены</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
            <button @click="copyAllIcons" class="btn btn-primary">
              <i class="fas fa-copy"></i>
              Копировать все
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SysOptions',
  data() {
    return {
      sysOptions: [],
      loading: false,
      error: null,
      limit: 25,
      offset: 0,
      pagination: {},
      
      // Font Awesome Icons данные
      fontAwesomeIcons: [],
      filteredIcons: [],
      iconSearchQuery: '',
      selectedStyle: 'all',
      selectedCategory: 'all',
      selectedColorScheme: 'default',
      selectedSize: 'base'
    }
  },
  mounted() {
    this.loadSysOptions()
    this.initializeFontAwesomeIcons()
  },
  methods: {
    canEditSysOption(option) {
      const currentUser = this.$currentUser
      if (!currentUser) return false
      // Пользователь может редактировать опцию, если он её создал или является администратором
      return option.user && option.user.id === currentUser.id || currentUser.is_staff || currentUser.is_superuser
    },
    async changePage(page) {
      if (page < 1) return
      
      // Проверяем, что страница в пределах допустимых значений
      if (this.pagination.total_pages && page > this.pagination.total_pages) return
      
      this.offset = (page - 1) * this.limit
      await this.loadSysOptions()
    },

    async goToFirstPage() {
      await this.changePage(1)
    },

    async goToLastPage() {
      if (this.pagination.total_pages) {
        await this.changePage(this.pagination.total_pages)
      }
    },

    async onLimitChange() {
      // Сбрасываем смещение на 0 при изменении лимита
      this.offset = 0
      await this.loadSysOptions()
    },
    async loadSysOptions() {
      this.loading = true
      this.error = null

      try {
        // Получаем CSRF токен из мета-тега
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value')

        const response = await fetch(`/api/sysoptions/?limit=${this.limit}&offset=${this.offset}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        this.sysOptions = data.results || data
        
        // Сохраняем информацию о пагинации если есть
        if (data.pagination) {
          this.pagination = data.pagination
        } else {
          this.pagination = {
            total_count: this.sysOptions.length,
            limit: this.limit,
            offset: this.offset,
            has_next: false,
            has_previous: this.offset > 0,
            current_page: 1,
            total_pages: 1
          }
        }
      } catch (error) {
        console.error('Error loading sysOptions:', error)
        this.error = 'Ошибка при загрузке данных: ' + error.message
      } finally {
        this.loading = false
      }
    },

    // Font Awesome Icons методы
    initializeFontAwesomeIcons() {
      // Популярные иконки Font Awesome с категориями
      const icons = [
        // Интерфейс
        { name: 'home', style: 'fas', category: 'interface', className: 'fas fa-home' },
        { name: 'user', style: 'fas', category: 'interface', className: 'fas fa-user' },
        { name: 'users', style: 'fas', category: 'interface', className: 'fas fa-users' },
        { name: 'cog', style: 'fas', category: 'interface', className: 'fas fa-cog' },
        { name: 'cogs', style: 'fas', category: 'interface', className: 'fas fa-cogs' },
        { name: 'settings', style: 'fas', category: 'interface', className: 'fas fa-sliders-h' },
        { name: 'bell', style: 'fas', category: 'interface', className: 'fas fa-bell' },
        { name: 'bell-slash', style: 'fas', category: 'interface', className: 'fas fa-bell-slash' },
        { name: 'calendar', style: 'fas', category: 'interface', className: 'fas fa-calendar' },
        { name: 'clock', style: 'fas', category: 'interface', className: 'fas fa-clock' },
        { name: 'calendar-alt', style: 'fas', category: 'interface', className: 'fas fa-calendar-alt' },
        { name: 'star', style: 'fas', category: 'interface', className: 'fas fa-star' },
        { name: 'heart', style: 'fas', category: 'interface', className: 'fas fa-heart' },
        { name: 'bookmark', style: 'fas', category: 'interface', className: 'fas fa-bookmark' },
        { name: 'tag', style: 'fas', category: 'interface', className: 'fas fa-tag' },
        { name: 'tags', style: 'fas', category: 'interface', className: 'fas fa-tags' },
        
        // Навигация
        { name: 'chevron-left', style: 'fas', category: 'navigation', className: 'fas fa-chevron-left' },
        { name: 'chevron-right', style: 'fas', category: 'navigation', className: 'fas fa-chevron-right' },
        { name: 'chevron-up', style: 'fas', category: 'navigation', className: 'fas fa-chevron-up' },
        { name: 'chevron-down', style: 'fas', category: 'navigation', className: 'fas fa-chevron-down' },
        { name: 'angle-left', style: 'fas', category: 'navigation', className: 'fas fa-angle-left' },
        { name: 'angle-right', style: 'fas', category: 'navigation', className: 'fas fa-angle-right' },
        { name: 'angle-up', style: 'fas', category: 'navigation', className: 'fas fa-angle-up' },
        { name: 'angle-down', style: 'fas', category: 'navigation', className: 'fas fa-angle-down' },
        { name: 'arrow-left', style: 'fas', category: 'navigation', className: 'fas fa-arrow-left' },
        { name: 'arrow-right', style: 'fas', category: 'navigation', className: 'fas fa-arrow-right' },
        { name: 'arrow-up', style: 'fas', category: 'navigation', className: 'fas fa-arrow-up' },
        { name: 'arrow-down', style: 'fas', category: 'navigation', className: 'fas fa-arrow-down' },
        { name: 'long-arrow-alt-left', style: 'fas', category: 'navigation', className: 'fas fa-long-arrow-alt-left' },
        { name: 'long-arrow-alt-right', style: 'fas', category: 'navigation', className: 'fas fa-long-arrow-alt-right' },
        { name: 'arrow-circle-left', style: 'fas', category: 'navigation', className: 'fas fa-arrow-circle-left' },
        { name: 'arrow-circle-right', style: 'fas', category: 'navigation', className: 'fas fa-arrow-circle-right' },
        
        // Медиа
        { name: 'play', style: 'fas', category: 'media', className: 'fas fa-play' },
        { name: 'pause', style: 'fas', category: 'media', className: 'fas fa-pause' },
        { name: 'stop', style: 'fas', category: 'media', className: 'fas fa-stop' },
        { name: 'forward', style: 'fas', category: 'media', className: 'fas fa-forward' },
        { name: 'backward', style: 'fas', category: 'media', className: 'fas fa-backward' },
        { name: 'volume-up', style: 'fas', category: 'media', className: 'fas fa-volume-up' },
        { name: 'volume-down', style: 'fas', category: 'media', className: 'fas fa-volume-down' },
        { name: 'volume-off', style: 'fas', category: 'media', className: 'fas fa-volume-off' },
        { name: 'video', style: 'fas', category: 'media', className: 'fas fa-video' },
        { name: 'camera', style: 'fas', category: 'media', className: 'fas fa-camera' },
        { name: 'image', style: 'fas', category: 'media', className: 'fas fa-image' },
        { name: 'photo', style: 'fas', category: 'media', className: 'fas fa-image' },
        { name: 'music', style: 'fas', category: 'media', className: 'fas fa-music' },
        { name: 'headphones', style: 'fas', category: 'media', className: 'fas fa-headphones' },
        { name: 'microphone', style: 'fas', category: 'media', className: 'fas fa-microphone' },
        
        // Формы
        { name: 'search', style: 'fas', category: 'forms', className: 'fas fa-search' },
        { name: 'plus', style: 'fas', category: 'forms', className: 'fas fa-plus' },
        { name: 'minus', style: 'fas', category: 'forms', className: 'fas fa-minus' },
        { name: 'times', style: 'fas', category: 'forms', className: 'fas fa-times' },
        { name: 'check', style: 'fas', category: 'forms', className: 'fas fa-check' },
        { name: 'edit', style: 'fas', category: 'forms', className: 'fas fa-edit' },
        { name: 'pencil-alt', style: 'fas', category: 'forms', className: 'fas fa-pencil-alt' },
        { name: 'trash', style: 'fas', category: 'forms', className: 'fas fa-trash' },
        { name: 'trash-alt', style: 'fas', category: 'forms', className: 'fas fa-trash-alt' },
        { name: 'copy', style: 'fas', category: 'forms', className: 'fas fa-copy' },
        { name: 'save', style: 'fas', category: 'forms', className: 'fas fa-save' },
        { name: 'download', style: 'fas', category: 'forms', className: 'fas fa-download' },
        { name: 'upload', style: 'fas', category: 'forms', className: 'fas fa-upload' },
        { name: 'eye', style: 'fas', category: 'forms', className: 'fas fa-eye' },
        { name: 'eye-slash', style: 'fas', category: 'forms', className: 'fas fa-eye-slash' },
        { name: 'lock', style: 'fas', category: 'forms', className: 'fas fa-lock' },
        { name: 'unlock', style: 'fas', category: 'forms', className: 'fas fa-unlock' },
        
        // Стрелки
        { name: 'arrow-circle-up', style: 'fas', category: 'arrows', className: 'fas fa-arrow-circle-up' },
        { name: 'arrow-circle-down', style: 'fas', category: 'arrows', className: 'fas fa-arrow-circle-down' },
        { name: 'caret-up', style: 'fas', category: 'arrows', className: 'fas fa-caret-up' },
        { name: 'caret-down', style: 'fas', category: 'arrows', className: 'fas fa-caret-down' },
        { name: 'caret-left', style: 'fas', category: 'arrows', className: 'fas fa-caret-left' },
        { name: 'caret-right', style: 'fas', category: 'arrows', className: 'fas fa-caret-right' },
        { name: 'sort', style: 'fas', category: 'arrows', className: 'fas fa-sort' },
        { name: 'sort-up', style: 'fas', category: 'arrows', className: 'fas fa-sort-up' },
        { name: 'sort-down', style: 'fas', category: 'arrows', className: 'fas fa-sort-down' },
        
        // Объекты
        { name: 'file', style: 'fas', category: 'objects', className: 'fas fa-file' },
        { name: 'file-alt', style: 'fas', category: 'objects', className: 'fas fa-file-alt' },
        { name: 'file-pdf', style: 'fas', category: 'objects', className: 'fas fa-file-pdf' },
        { name: 'file-word', style: 'fas', category: 'objects', className: 'fas fa-file-word' },
        { name: 'file-excel', style: 'fas', category: 'objects', className: 'fas fa-file-excel' },
        { name: 'file-powerpoint', style: 'fas', category: 'objects', className: 'fas fa-file-powerpoint' },
        { name: 'file-image', style: 'fas', category: 'objects', className: 'fas fa-file-image' },
        { name: 'folder', style: 'fas', category: 'objects', className: 'fas fa-folder' },
        { name: 'folder-open', style: 'fas', category: 'objects', className: 'fas fa-folder-open' },
        { name: 'archive', style: 'fas', category: 'objects', className: 'fas fa-archive' },
        { name: 'book', style: 'fas', category: 'objects', className: 'fas fa-book' },
        { name: 'bookmark', style: 'fas', category: 'objects', className: 'fas fa-bookmark' },
        { name: 'certificate', style: 'fas', category: 'objects', className: 'fas fa-certificate' },
        { name: 'gift', style: 'fas', category: 'objects', className: 'fas fa-gift' },
        { name: 'leaf', style: 'fas', category: 'objects', className: 'fas fa-leaf' },
        
        // Текст
        { name: 'font', style: 'fas', category: 'text', className: 'fas fa-font' },
        { name: 'bold', style: 'fas', category: 'text', className: 'fas fa-bold' },
        { name: 'italic', style: 'fas', category: 'text', className: 'fas fa-italic' },
        { name: 'underline', style: 'fas', category: 'text', className: 'fas fa-underline' },
        { name: 'strikethrough', style: 'fas', category: 'text', className: 'fas fa-strikethrough' },
        { name: 'align-left', style: 'fas', category: 'text', className: 'fas fa-align-left' },
        { name: 'align-center', style: 'fas', category: 'text', className: 'fas fa-align-center' },
        { name: 'align-right', style: 'fas', category: 'text', className: 'fas fa-align-right' },
        { name: 'align-justify', style: 'fas', category: 'text', className: 'fas fa-align-justify' },
        { name: 'list', style: 'fas', category: 'text', className: 'fas fa-list' },
        { name: 'list-ul', style: 'fas', category: 'text', className: 'fas fa-list-ul' },
        { name: 'list-ol', style: 'fas', category: 'text', className: 'fas fa-list-ol' },
        
        // Транспорт
        { name: 'car', style: 'fas', category: 'transportation', className: 'fas fa-car' },
        { name: 'truck', style: 'fas', category: 'transportation', className: 'fas fa-truck' },
        { name: 'bus', style: 'fas', category: 'transportation', className: 'fas fa-bus' },
        { name: 'train', style: 'fas', category: 'transportation', className: 'fas fa-train' },
        { name: 'plane', style: 'fas', category: 'transportation', className: 'fas fa-plane' },
        { name: 'ship', style: 'fas', category: 'transportation', className: 'fas fa-ship' },
        { name: 'bicycle', style: 'fas', category: 'transportation', className: 'fas fa-bicycle' },
        { name: 'motorcycle', style: 'fas', category: 'transportation', className: 'fas fa-motorcycle' },
        
        // Гендер
        { name: 'male', style: 'fas', category: 'gender', className: 'fas fa-male' },
        { name: 'female', style: 'fas', category: 'gender', className: 'fas fa-female' },
        { name: 'genderless', style: 'fas', category: 'gender', className: 'fas fa-genderless' },
        { name: 'transgender', style: 'fas', category: 'gender', className: 'fas fa-transgender' },
        { name: 'transgender-alt', style: 'fas', category: 'gender', className: 'fas fa-transgender-alt' },
        { name: 'venus', style: 'fas', category: 'gender', className: 'fas fa-venus' },
        { name: 'mars', style: 'fas', category: 'gender', className: 'fas fa-mars' },
        { name: 'intersex', style: 'fas', category: 'gender', className: 'fas fa-intersex' },
        
        // Платежи
        { name: 'credit-card', style: 'fas', category: 'payment', className: 'fas fa-credit-card' },
        { name: 'money-check', style: 'fas', category: 'payment', className: 'fas fa-money-check' },
        { name: 'dollar-sign', style: 'fas', category: 'payment', className: 'fas fa-dollar-sign' },
        { name: 'euro-sign', style: 'fas', category: 'payment', className: 'fas fa-euro-sign' },
        { name: 'pound-sign', style: 'fas', category: 'payment', className: 'fas fa-pound-sign' },
        { name: 'yen-sign', style: 'fas', category: 'payment', className: 'fas fa-yen-sign' },
        { name: 'rupee-sign', style: 'fas', category: 'payment', className: 'fas fa-rupee-sign' },
        
        // Диаграммы
        { name: 'chart-bar', style: 'fas', category: 'charts', className: 'fas fa-chart-bar' },
        { name: 'chart-line', style: 'fas', category: 'charts', className: 'fas fa-chart-line' },
        { name: 'chart-pie', style: 'fas', category: 'charts', className: 'fas fa-chart-pie' },
        { name: 'chart-area', style: 'fas', category: 'charts', className: 'fas fa-chart-area' },
        
        // Валюта
        { name: 'bitcoin', style: 'fab', category: 'currency', className: 'fab fa-bitcoin' },
        { name: 'ethereum', style: 'fab', category: 'currency', className: 'fab fa-ethereum' },
        { name: 'dollar', style: 'fas', category: 'currency', className: 'fas fa-dollar-sign' },
        { name: 'euro', style: 'fas', category: 'currency', className: 'fas fa-euro-sign' },
        { name: 'pound', style: 'fas', category: 'currency', className: 'fas fa-pound-sign' },
        { name: 'yen', style: 'fas', category: 'currency', className: 'fas fa-yen-sign' },
        { name: 'ruble', style: 'fas', category: 'currency', className: 'fas fa-ruble-sign' },
        
        // Время
        { name: 'clock', style: 'fas', category: 'time', className: 'fas fa-clock' },
        { name: 'hourglass', style: 'fas', category: 'time', className: 'fas fa-hourglass' },
        { name: 'calendar', style: 'fas', category: 'time', className: 'fas fa-calendar' },
        { name: 'calendar-check', style: 'fas', category: 'time', className: 'fas fa-calendar-check' },
        
        // Медицина
        { name: 'stethoscope', style: 'fas', category: 'medical', className: 'fas fa-stethoscope' },
        { name: 'heartbeat', style: 'fas', category: 'medical', className: 'fas fa-heartbeat' },
        { name: 'ambulance', style: 'fas', category: 'medical', className: 'fas fa-ambulance' },
        { name: 'hospital', style: 'fas', category: 'medical', className: 'fas fa-hospital' },
        { name: 'pills', style: 'fas', category: 'medical', className: 'fas fa-pills' },
        { name: 'syringe', style: 'fas', category: 'medical', className: 'fas fa-syringe' },
        
        // Доступность
        { name: 'universal-access', style: 'fas', category: 'accessibility', className: 'fas fa-universal-access' },
        { name: 'blind', style: 'fas', category: 'accessibility', className: 'fas fa-blind' },
        { name: 'deaf', style: 'fas', category: 'accessibility', className: 'fas fa-deaf' },
        { name: 'sign-language', style: 'fas', category: 'accessibility', className: 'fas fa-sign-language' },
        
        // Прочие
        { name: 'info', style: 'fas', category: 'other', className: 'fas fa-info-circle' },
        { name: 'question', style: 'fas', category: 'other', className: 'fas fa-question-circle' },
        { name: 'exclamation', style: 'fas', category: 'other', className: 'fas fa-exclamation-circle' },
        { name: 'exclamation-triangle', style: 'fas', category: 'other', className: 'fas fa-exclamation-triangle' },
        { name: 'warning', style: 'fas', category: 'other', className: 'fas fa-exclamation-triangle' },
        { name: 'shield', style: 'fas', category: 'other', className: 'fas fa-shield-alt' },
        { name: 'shield-alt', style: 'fas', category: 'other', className: 'fas fa-shield-alt' }
      ]
      
      this.fontAwesomeIcons = icons
      this.filteredIcons = [...icons]
    },

    showFontAwesomeModal() {
      // Используем Bootstrap модальное окно
      $('#fontAwesomeModal').modal('show')
      this.filterIcons()
    },

    filterIcons() {
      let filtered = [...this.fontAwesomeIcons]
      
      // Фильтр по поисковому запросу
      if (this.iconSearchQuery.trim()) {
        const query = this.iconSearchQuery.toLowerCase()
        filtered = filtered.filter(icon =>
          icon.name.toLowerCase().includes(query) ||
          icon.category.toLowerCase().includes(query)
        )
      }
      
      // Фильтр по стилю
      if (this.selectedStyle !== 'all') {
        filtered = filtered.filter(icon => icon.style === this.selectedStyle)
      }
      
      // Фильтр по категории
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(icon => icon.category === this.selectedCategory)
      }
      
      this.filteredIcons = filtered
    },

    getIconClasses(icon) {
      const classes = ['icon-wrapper']
      
      // Добавляем класс цвета
      if (this.selectedColorScheme !== 'default') {
        classes.push(`text-${this.selectedColorScheme}`)
      }
      
      // Добавляем класс размера
      if (this.selectedSize !== 'base') {
        classes.push(`fa-${this.selectedSize}`)
      }
      
      return classes.join(' ')
    },

    copyIconCode(icon) {
      const code = `<i class="${icon.className}"></i>`
      navigator.clipboard.writeText(code).then(() => {
        // Временное уведомление
        const originalTitle = icon.name
        icon.name = 'Скопировано!'
        setTimeout(() => {
          icon.name = originalTitle
        }, 1000)
      }).catch(err => {
        console.error('Не удалось скопировать код: ', err)
      })
    },

    copyAllIcons() {
      const allCodes = this.filteredIcons.map(icon =>
        `<!-- ${icon.name} -->\n<i class="${icon.className}"></i>`
      ).join('\n')
      
      navigator.clipboard.writeText(allCodes).then(() => {
        alert(`Скопировано ${this.filteredIcons.length} иконок в буфер обмена!`)
      }).catch(err => {
        console.error('Не удалось скопировать все иконки: ', err)
      })
    }
  }
}
</script>

<style scoped>
.table th {
  vertical-align: middle;
}

.badge {
  font-size: 0.8em;
}

code {
  font-size: 0.85em;
  word-break: break-all;
}

.icon-wrapper {
  display: block;
  margin-bottom: 10px;
}

.hover-effect {
  transition: all 0.3s ease;
  cursor: pointer;
}

.hover-effect:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.modal-xl {
  max-width: 90%;
}

.cursor-pointer {
  cursor: pointer;
}

/* Font Awesome размеры */
.fa-xs { font-size: 0.75em; }
.fa-sm { font-size: 0.875em; }
.fa-lg { font-size: 1.33333em; }
.fa-2x { font-size: 2em; }
.fa-3x { font-size: 3em; }
.fa-4x { font-size: 4em; }
.fa-5x { font-size: 5em; }
.fa-6x { font-size: 6em; }
.fa-7x { font-size: 7em; }
.fa-8x { font-size: 8em; }
.fa-9x { font-size: 9em; }
.fa-10x { font-size: 10em; }

/* Цветовые схемы */
.text-primary { color: #007bff !important; }
.text-success { color: #28a745 !important; }
.text-warning { color: #ffc107 !important; }
.text-danger { color: #dc3545 !important; }
.text-info { color: #17a2b8 !important; }
.text-muted { color: #6c757d !important; }

@media (max-width: 768px) {
  .modal-xl {
    max-width: 95%;
    margin: 10px auto;
  }
}
</style>