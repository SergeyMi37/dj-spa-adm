<template>
  <div class="row">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Список параметров</h3>
          <div class="card-tools">
            <button @click="loadParams" class="btn btn-primary btn-sm" :disabled="loading">
              <i class="fas fa-sync"></i>
              {{ loading ? 'Загрузка...' : 'Обновить' }}
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

          <div v-if="params.length > 0" class="table-responsive">
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
                <tr v-for="param in params" :key="param.id">
                  <td>{{ param.id }}</td>
                  <td><strong>{{ param.name }}</strong></td>
                  <td>
                    <span class="badge badge-info">{{ param.category }}</span>
                  </td>
                  <td>{{ param.desc || '-' }}</td>
                  <td>{{ param.option || '-' }}</td>
                  <td>
                    <code v-if="param.json" class="text-muted small">{{ param.json }}</code>
                    <span v-else>-</span>
                  </td>
                  <td>
                    <span class="badge" :class="param.public ? 'badge-success' : 'badge-secondary'">
                      <i :class="param.public ? 'fas fa-check' : 'fas fa-times'"></i>
                      {{ param.public ? 'Да' : 'Нет' }}
                    </span>
                  </td>
                  <td>{{ param.user ? param.user.username : 'Система' }}</td>
                  <td>
                    <span v-if="canEditParam(param)" class="badge badge-success">
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
            <i class="fas fa-list fa-3x mb-3"></i>
            <p>Нажмите "Обновить" для загрузки списка параметров</p>
          </div>

          <div v-if="error" class="alert alert-danger mt-3">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Ошибка:</strong> {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Params',
  data() {
    return {
      params: [],
      loading: false,
      error: null,
      limit: 25,
      offset: 0,
      pagination: {}
    }
  },
  mounted() {
    this.loadParams()
  },
  methods: {
    canEditParam(param) {
      const currentUser = this.$currentUser
      if (!currentUser) return false
      // Пользователь может редактировать параметр, если он его создал или является администратором
      return param.user && param.user.id === currentUser.id || currentUser.is_staff || currentUser.is_superuser
    },
    async changePage(page) {
      if (page < 1) return
      
      // Проверяем, что страница в пределах допустимых значений
      if (this.pagination.total_pages && page > this.pagination.total_pages) return
      
      this.offset = (page - 1) * this.limit
      await this.loadParams()
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
      await this.loadParams()
    },
    async loadParams() {
      this.loading = true
      this.error = null

      try {
        // Получаем CSRF токен из мета-тега
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value')

        const response = await fetch(`/api/params/?limit=${this.limit}&offset=${this.offset}`, {
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
        this.params = data.results || data
        
        // Сохраняем информацию о пагинации если есть
        if (data.pagination) {
          this.pagination = data.pagination
        } else {
          this.pagination = {
            total_count: this.params.length,
            limit: this.limit,
            offset: this.offset,
            has_next: false,
            has_previous: this.offset > 0,
            current_page: 1,
            total_pages: 1
          }
        }
      } catch (error) {
        console.error('Error loading params:', error)
        this.error = 'Ошибка при загрузке данных: ' + error.message
      } finally {
        this.loading = false
      }
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
</style>