<template>
  <div class="container">
    <!-- Модальное окно настроек подключений к БД -->
    <div v-if="showConnectionSettings" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0,0,0,0.5);" @click="closeModal">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-database"></i>
              Настройки подключений к БД
            </h5>
            <button
              @click.stop="closeModal"
              type="button"
              class="btn-close"
              aria-label="Закрыть"
            ></button>
          </div>
          <div class="modal-body">
            <div v-if="modalError" class="alert alert-danger mb-3">
              {{ modalError }}
            </div>
            
            <!-- Список сохраненных подключений - перемещен в начало -->
            <div class="row mb-4">
              <div class="col-12">
                <div class="input-group">
                  <select
                    id="savedConnections"
                    v-model="selectedConnectionId"
                    class="form-control"
                    @change="onConnectionSelectChange"
                  >
                    <option value="">Выберите подключение...</option>
                    <option
                      v-for="conn in savedConnections"
                      :key="conn.id"
                      :value="conn.id"
                    >
                      {{ conn.name }} ({{ conn.databaseType.toUpperCase() }})
                    </option>
                  </select>
                  <div class="input-group-append">
                    <button
                      @click="deleteConnection"
                      class="btn btn-outline-danger"
                      :disabled="!selectedConnectionId"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="databaseType" class="form-label">Тип базы данных:</label>
                <select
                  id="databaseType"
                  v-model="selectedConnection.databaseType"
                  class="form-control"
                  @change="onDatabaseTypeChange"
                >
                  <option value="postgresql">PostgreSQL</option>
                  <option value="oracle">Oracle</option>
                  <option value="iris">IRIS</option>
                </select>
              </div>
              <div class="col-md-6">
                <label for="connectionName" class="form-label">Имя подключения:</label>
                <input
                  id="connectionName"
                  v-model="selectedConnection.name"
                  type="text"
                  class="form-control"
                  placeholder="Например: Основная БД"
                >
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-12">
                <label for="connectionString" class="form-label">
                  Строка подключения JDBC:
                  <small v-if="selectedConnection.databaseType === 'iris'" class="text-info">
                    <i class="fas fa-info-circle"></i>
                    Формат: jdbc:IRIS://host:port/NAMESPACE
                  </small>
                  <small v-else-if="selectedConnection.databaseType === 'postgresql'" class="text-info">
                    <i class="fas fa-info-circle"></i>
                    Формат: jdbc:postgresql://host:port/database
                  </small>
                  <small v-else-if="selectedConnection.databaseType === 'oracle'" class="text-info">
                    <i class="fas fa-info-circle"></i>
                    Формат: jdbc:oracle:thin:@host:port:service
                  </small>
                </label>
                <input
                  id="connectionString"
                  v-model="selectedConnection.connectionString"
                  type="text"
                  class="form-control"
                  :placeholder="getConnectionPlaceholder()"
                >
                <small v-if="selectedConnection.databaseType === 'iris'" class="form-text text-muted">
                  <strong>Примеры:</strong><br>
                  • jdbc:IRIS://localhost:1972/USER<br>
                  • jdbc:IRIS://iris-server:1972/SAMPLES<br>
                  • jdbc:IRIS://192.168.1.100:1972/PRODUCTION
                </small>
                <small v-else-if="selectedConnection.databaseType === 'postgresql'" class="form-text text-muted">
                  <strong>Примеры:</strong><br>
                  • jdbc:postgresql://localhost:5432/mydb<br>
                  • jdbc:postgresql://192.168.1.100:5432/proddb<br>
                  • jdbc:postgresql://pg-server:5432/testdb
                </small>
                <small v-else-if="selectedConnection.databaseType === 'oracle'" class="form-text text-muted">
                  <strong>Примеры:</strong><br>
                  • jdbc:oracle:thin:@localhost:1521:XE<br>
                  • jdbc:oracle:thin:@//localhost:1521/XEPDB1<br>
                  • jdbc:oracle:thin:@server:1521:PROD
                </small>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="connectionUsername" class="form-label">Пользователь:</label>
                <input
                  id="connectionUsername"
                  v-model="selectedConnection.username"
                  type="text"
                  class="form-control"
                  placeholder="username"
                >
              </div>
              <div class="col-md-6">
                <label for="connectionPassword" class="form-label">Пароль:</label>
                <input
                  id="connectionPassword"
                  v-model="selectedConnection.password"
                  type="text"
                  class="form-control"
                  placeholder="password"
                >
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-12 d-flex justify-content-end">
                <button @click="testConnection" class="btn btn-info mr-2" :disabled="loading">
                  <i class="fas fa-plug"></i>
                  Тест подключения
                </button>
                <button @click="saveConnection" class="btn btn-success mr-2">
                  <i class="fas fa-save"></i>
                  Сохранить
                </button>
                <button @click="closeModal" type="button" class="btn btn-secondary">
                  <i class="fas fa-times"></i>
                  Закрыть
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Основная область запросов -->
    <div class="mb-3">

      <!-- История SQL запросов -->
      <div v-if="queryHistory.length > 0" class="mb-2">
        <label for="queryHistory" class="form-label small text-muted">
          <i class="fas fa-history"></i>
          История SQL запросов:
        </label>
        <select
          id="queryHistory"
          v-model="selectedHistoryQuery"
          @change="onHistoryQuerySelect"
          class="form-control form-control-sm"
        >
          <option value="">Выберите из истории...</option>
          <option
            v-for="(query, index) in queryHistory"
            :key="index"
            :value="query"
          >
            {{ query.length > 100 ? query.substring(0, 100) + '...' : query }}
          </option>
        </select>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-2">
        <button @click="executeQuery" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Выполняется...' : 'Выполнить запрос' }}
        </button>
        <div class="d-flex gap-2 align-items-center">
          <button @click="clearSqlQuery" class="btn btn-outline-danger btn-sm" title="Очистить запрос">
            <i class="fas fa-times"></i> Очистить
          </button>
          <button
            @click="openConnectionSettings"
            class="btn btn-outline-primary btn-sm"
          >
            <i class="fas fa-cog"></i>
            Настройки
          </button>
          <div class="d-flex align-items-center ms-2">
            <select
              id="activeConnection"
              v-model="activeConnectionId"
              class="form-control form-control-sm"
              style="width: auto; min-width: 200px;"
              @change="onActiveConnectionChange"
            >
              <option value="">БД по умолчанию</option>
              <option
                v-for="conn in savedConnections"
                :key="conn.id"
                :value="conn.id"
              >
                {{ conn.name }} ({{ conn.databaseType.toUpperCase() }})
              </option>
            </select>
          </div>
        </div>
      </div>
      <textarea
        id="sqlQuery"
        v-model="sqlQuery"
        class="form-control"
        rows="5"
        placeholder="Введите SQL запрос... (Ctrl+Enter для выполнения)"
        @keydown.enter.ctrl="executeQuery"
      ></textarea>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>

    <div v-if="results.length > 0" class="mt-3">
      <div class="mb-3">
        <h7>Результат:</h7>
        <div class="mb-2">
          <small class="text-muted">
            Показано {{ results.length }} из {{ pagination.total_count || results.length }} записей
            <span v-if="pagination.total_pages > 1">
              (Страница {{ pagination.current_page }} из {{ pagination.total_pages }})
            </span>
          </small>
        </div>
        
        <!-- Объединенный пагинатор с селектором количества записей -->
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
      </div>
      
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th v-for="column in columns" :key="column">{{ column }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in results" :key="index">
              <td v-for="value in row" :key="value">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DbQueries',
  data() {
    return {
      sqlQuery: '',
      results: [],
      columns: [],
      loading: false,
      error: null,
      limit: 5,
      offset: 0,
      pagination: {},
      queryHistory: [],
      selectedHistoryQuery: '',
      
      // Настройки подключений
      showConnectionSettings: false,
      showPassword: false,
      selectedConnectionId: '',
      activeConnectionId: '',
      savedConnections: [],
      modalError: null,
      selectedConnection: {
        id: '',
        name: '',
        originalName: '', // Для отслеживания изменений имени
        databaseType: 'postgresql',
        connectionString: '',
        username: '',
        password: ''
      }
    };
  },
  mounted() {
    // Загружаем историю SQL запросов при инициализации
    this.loadQueryHistory();
    // Загружаем сохраненные подключения
    this.loadSavedConnections();
  },
  methods: {
    async executeQuery() {
      if (!this.sqlQuery.trim()) {
        this.error = 'Введите SQL запрос';
        return;
      }

      // Сохраняем запрос в историю СРАЗУ перед выполнением
      this.saveQueryToHistory(this.sqlQuery.trim());

      this.loading = true;
      this.error = null;
      this.results = [];
      this.columns = [];

      try {
        const requestData = {
          query: this.sqlQuery,
          limit: this.limit,
          offset: this.offset
        };
        
        // Добавляем информацию о подключении если выбрано
        if (this.activeConnectionId) {
          requestData.connectionId = this.activeConnectionId;
        }

        const response = await axios.post('/api/db-queries/', requestData, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (response.data.columns && response.data.rows) {
          this.columns = response.data.columns;
          this.results = response.data.rows;
          
          // Сохраняем информацию о пагинации
          if (response.data.pagination) {
            this.pagination = response.data.pagination;
          } else {
            this.pagination = {
              total_count: this.results.length,
              limit: this.limit,
              offset: this.offset,
              has_next: false,
              has_previous: this.offset > 0,
              current_page: 1,
              total_pages: 1
            };
          }
        } else if (response.data.message) {
          // Для команд, которые не возвращают данные
          this.error = null;
          this.results = [];
          this.columns = [];
          this.pagination = {};
          alert(response.data.message + (response.data.affected_rows ? ` (затронуто строк: ${response.data.affected_rows})` : ''));
        } else {
          this.error = 'Неверный формат ответа от сервера';
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка выполнения запроса';
        this.results = [];
        this.columns = [];
        this.pagination = {};
      } finally {
        this.loading = false;
      }
    },

    async testConnection() {
      this.modalError = null;
      
      if (!this.selectedConnection.connectionString) {
        this.modalError = 'Заполните строку подключения';
        return;
      }

      this.loading = true;
      this.modalError = null;

      try {
        const response = await axios.post('/api/db-connections/test-connection/', {
          connection: {
            databaseType: this.selectedConnection.databaseType,
            connection_string: this.selectedConnection.connectionString,
            username: this.selectedConnection.username,
            password: this.selectedConnection.password
          }
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (response.data.success) {
          alert('Подключение успешно!');
          this.closeModal();
        } else {
          this.modalError = 'Ошибка подключения: ' + (response.data.error || 'Неизвестная ошибка');
        }
      } catch (err) {
        this.modalError = 'Ошибка тестирования подключения: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async saveConnection() {
      this.modalError = null;
      
      if (!this.selectedConnection.name || !this.selectedConnection.connectionString || !this.selectedConnection.username || !this.selectedConnection.password) {
        this.modalError = 'Заполните все поля формы';
        return;
      }

      this.loading = true;
      this.modalError = null;

      try {
        const csrftoken = this.getCookie('csrftoken');
        
        console.log('💾 Saving connection:', {
          id: this.selectedConnection.id,
          name: this.selectedConnection.name,
          originalName: this.selectedConnection.originalName,
          nameChanged: this.selectedConnection.name !== this.selectedConnection.originalName
        });
        
        if (this.selectedConnection.id && this.selectedConnection.name === this.selectedConnection.originalName) {
          console.log('📝 Updating existing connection (name unchanged)');
          
          // Обновление существующего подключения (имя не изменилось)
          const response = await axios.put(`/api/db-connections/${this.selectedConnection.id}/`, {
            name: this.selectedConnection.name,
            database_type: this.selectedConnection.databaseType,
            connection_string: this.selectedConnection.connectionString,
            username: this.selectedConnection.username,
            password: this.selectedConnection.password,
            description: this.selectedConnection.description,
            is_active: true
          }, {
            headers: {
              'X-CSRFToken': csrftoken
            }
          });

          alert('Подключение обновлено!');
          this.closeModal();
        } else {
          console.log('➕ Creating new connection (name changed or new connection)');
          
          // Создание нового подключения
          const response = await axios.post('/api/db-connections/', {
            name: this.selectedConnection.name,
            database_type: this.selectedConnection.databaseType,
            connection_string: this.selectedConnection.connectionString,
            username: this.selectedConnection.username,
            password: this.selectedConnection.password,
            description: this.selectedConnection.description,
            is_active: true
          }, {
            headers: {
              'X-CSRFToken': csrftoken
            }
          });

          const actionText = this.selectedConnection.id ? 'создано новое подключение' : 'сохранено';
          alert(`Подключение ${actionText}!`);
          this.closeModal();
        }
        
        // Обновляем список сохраненных подключений
        this.loadSavedConnections();
        
        // Очищаем форму для нового подключения
        this.selectedConnection = {
          id: '',
          name: '',
          originalName: '',
          databaseType: 'postgresql',
          connectionString: '',
          username: '',
          password: ''
        };
        
      } catch (err) {
        this.modalError = 'Ошибка сохранения подключения: ' + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async deleteConnection() {
      if (!this.selectedConnectionId) return;
      
      if (!confirm('Вы уверены, что хотите удалить это подключение?')) return;

      try {
        const response = await axios.delete(`/api/db-connections/${this.selectedConnectionId}/`, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.loadSavedConnections();
        this.selectedConnectionId = '';
        if (this.activeConnectionId === this.selectedConnectionId) {
          this.activeConnectionId = '';
        }
        alert('Подключение удалено!');
      } catch (err) {
        this.error = 'Ошибка удаления подключения: ' + (err.response?.data?.error || err.message);
      }
    },

    openConnectionSettings() {
      console.log('🚀 openConnectionSettings called');
      this.showConnectionSettings = true;
      this.modalError = null;
      
      // Обновляем список подключений при каждом открытии модального окна
      this.loadSavedConnections();
      
      console.log('🚀 Modal opened, current selectedConnectionId:', this.selectedConnectionId);
      console.log('🚀 Available connections in modal:', this.savedConnections);
    },

    onConnectionSelectChange() {
      console.log('🔄 onConnectionSelectChange called');
      console.log('📝 Selected connection ID:', this.selectedConnectionId);
      console.log('📋 Available connections:', this.savedConnections);
      
      if (!this.selectedConnectionId) {
        console.log('⚠️ No connection ID selected');
        return;
      }
      
      this.loadConnection();
    },

    loadConnection() {
      console.log('🔄 loadConnection called with ID:', this.selectedConnectionId);
      
      if (!this.selectedConnectionId) {
        console.log('⚠️ No selectedConnectionId, exiting');
        return;
      }
      
      this.modalError = null;
      
      const connection = this.savedConnections.find(conn => conn.id == this.selectedConnectionId);
      console.log('🔍 Found connection:', connection);
      
      if (connection) {
        console.log('📤 Found connection, loading as-is from database');
        console.log('📤 Full connection object:', connection);
        console.log('📤 Connection password value:', connection.password);
        console.log('📤 Connection keys:', Object.keys(connection));
        
        // Загружаем данные точно как в базе
        this.selectedConnection = {
          id: connection.id,
          name: connection.name,
          originalName: connection.name, // Сохраняем оригинальное имя для отслеживания изменений
          databaseType: connection.databaseType,
          connectionString: connection.connectionString, // ТОЧНО как в БД
          username: connection.username,
          password: connection.password // Заполняем поле пароля для удобства
        };
        
        console.log('✅ selectedConnection after update:', this.selectedConnection);
        console.log('✅ selectedConnection password:', this.selectedConnection.password);
      } else {
        console.log('❌ Connection not found for ID:', this.selectedConnectionId);
      }
    },

    async loadSavedConnections() {
      console.log('📥 loadSavedConnections called');
      
      try {
        const response = await axios.get('/api/db-connections/', {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        console.log('📥 Raw response data:', response.data);
        
        this.savedConnections = response.data.results || response.data || [];
        console.log('📥 After extracting from response:', this.savedConnections);
        
        // Логируем первую запись для диагностики password
        if (this.savedConnections.length > 0) {
          console.log('📥 First connection raw data:', this.savedConnections[0]);
          console.log('📥 First connection password value:', this.savedConnections[0].password);
          console.log('📥 First connection keys:', Object.keys(this.savedConnections[0]));
        }
        
        this.savedConnections = this.savedConnections.map(conn => ({
          id: conn.id,
          name: conn.name,
          databaseType: conn.database_type,
          connectionString: conn.connection_string,
          username: conn.username,
          password: conn.password, // ТОЧНО как в БД
          description: conn.description,
          isActive: conn.is_active,
          createdDate: conn.created_date,
          updatedDate: conn.updated_date
        }));
        
        console.log('📥 Final transformed connections:', this.savedConnections);
        
        // Логируем первую запись после трансформации
        if (this.savedConnections.length > 0) {
          console.log('📥 First connection after transform:', this.savedConnections[0]);
          console.log('📥 First connection password after transform:', this.savedConnections[0].password);
        }
      } catch (err) {
        console.warn('❌ Не удалось загрузить сохраненные подключения:', err);
        this.savedConnections = [];
        console.log('📥 Set empty connections array:', this.savedConnections);
      }
    },

    onDatabaseTypeChange() {
      // Обновляем placeholder при смене типа БД
      this.selectedConnection.connectionString = '';
    },

    getConnectionPlaceholder() {
      if (this.selectedConnection.databaseType === 'postgresql') {
        return 'jdbc:postgresql://localhost:5432/database_name';
      } else if (this.selectedConnection.databaseType === 'oracle') {
        return 'jdbc:oracle:thin:@localhost:1521:XE';
      } else if (this.selectedConnection.databaseType === 'iris') {
        return 'jdbc:IRIS://localhost:1972/USER';
      } else {
        return 'jdbc:your-database://host:port/database';
      }
    },

    onActiveConnectionChange() {
      // Логика смены активного подключения
      console.log('Активное подключение изменено:', this.activeConnectionId);
    },

    async changePage(page) {
      if (page < 1) return;
      
      // Проверяем, что страница в пределах допустимых значений
      if (this.pagination.total_pages && page > this.pagination.total_pages) return;
      
      this.offset = (page - 1) * this.limit;
      await this.executeQuery();
      
      // Прокручиваем страницу к началу результатов
      this.$nextTick(() => {
        const resultsElement = document.querySelector('.mt-3 h7');
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth' });
        }
      });
    },

    async onLimitChange() {
      // Сбрасываем смещение на 0 при изменении лимита
      this.offset = 0;
      await this.executeQuery();
    },

    async goToFirstPage() {
      await this.changePage(1);
    },

    async goToLastPage() {
      if (this.pagination.total_pages) {
        await this.changePage(this.pagination.total_pages);
      }
    },

    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    onHistoryQuerySelect() {
      if (this.selectedHistoryQuery) {
        this.sqlQuery = this.selectedHistoryQuery;
        this.selectedHistoryQuery = '';
      }
    },

    saveQueryToHistory(query) {
      try {
        // Проверяем, нет ли уже такого запроса в истории
        if (!this.queryHistory.includes(query)) {
          // Добавляем в начало массива
          this.queryHistory.unshift(query);
          
          // Ограничиваем историю 50 запросами
          if (this.queryHistory.length > 50) {
            this.queryHistory = this.queryHistory.slice(0, 50);
          }
          
          // Сохраняем в localStorage
          localStorage.setItem('dbQueries_history', JSON.stringify(this.queryHistory));
        }
      } catch (e) {
        console.warn('Не удалось сохранить SQL запрос в историю:', e);
      }
    },

    loadQueryHistory() {
      try {
        const saved = localStorage.getItem('dbQueries_history');
        if (saved) {
          this.queryHistory = JSON.parse(saved);
        }
      } catch (e) {
        console.warn('Не удалось загрузить историю SQL запросов:', e);
        this.queryHistory = [];
      }
    },

    clearSqlQuery() {
      this.sqlQuery = '';
      this.error = null;
      this.results = [];
      this.columns = [];
      this.pagination = {};
    },

    parseConnectionString(connectionString) {
      // Парсим строку JDBC подключения для извлечения username и password
      // Поддерживаем форматы:
      // jdbc:postgresql://user:password@host:port/database
      // jdbc:oracle:thin:user/password@host:port:database
      
      try {
        // Извлекаем часть с аутентификацией
        const authMatch = connectionString.match(/:\/\/([^@\/\s:]+):([^@\/\s]+)@/);
        
        if (authMatch) {
          return {
            username: authMatch[1],
            password: authMatch[2]
          };
        }
        
        // Для Oracle формата thin:user/password@
        const oracleMatch = connectionString.match(/thin:([^@\/]+)\/([^@]+)@/);
        if (oracleMatch) {
          return {
            username: oracleMatch[1],
            password: oracleMatch[2]
          };
        }
        
        // Если не удалось извлечь, возвращаем пустые значения
        return {
          username: '',
          password: ''
        };
      } catch (e) {
        console.error('Ошибка парсинга строки подключения:', e);
        return {
          username: '',
          password: ''
        };
      }
    },

    closeModal() {
      this.showConnectionSettings = false;
      this.modalError = null;
      this.error = null;
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.badge-info {
  background-color: #17a2b8;
  color: white;
}

.btn:disabled {
  cursor: not-allowed;
}

.text-muted {
  color: #6c757d !important;
}

/* Стили для объединенного пагинатора */
.border.rounded.bg-light {
  border-color: #dee2e6 !important;
  background-color: #f8f9fa !important;
}

.form-control {
  font-size: 14px;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 14px;
}

@media (max-width: 768px) {
  .d-flex.justify-content-between.align-items-center {
    flex-direction: column;
    gap: 10px;
  }
  
  .d-flex.align-items-center {
    flex-direction: column;
    gap: 8px;
  }
  
  .form-control {
    width: 100% !important;
    max-width: 200px;
  }
}

/* Стили для активного состояния кнопок */
.btn:active {
  color: #e9ecef !important;
}

.btn-outline-primary:active {
  color: #f8f9fa !important;
}

.btn-outline-secondary:active {
  color: #f8f9fa !important;
}
</style>