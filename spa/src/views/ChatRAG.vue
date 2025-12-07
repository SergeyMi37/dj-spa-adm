<template>
  <div class="container">
    <div class="chat-container">
      <!-- Заголовок чата -->
      <div class="chat-header mb-3">
        <h5>
          <i class="fas fa-comments"></i>
          Диалог с RAG-ассистентом
        </h5>
        <small class="text-muted">
          Задайте вопрос о ваших данных, и ассистент найдет релевантную информацию
        </small>
        
        <!-- Форма выбора модели -->
        <div class="model-selector mt-3">
          <div class="row align-items-center">
            <div class="col-md-6">
              <label for="modelSelect" class="form-label">
                <i class="fas fa-robot"></i>
                Выберите модель:
              </label>
              <select
                id="modelSelect"
                v-model="selectedModel"
                class="form-control"
                :disabled="modelsLoading"
                @change="onModelChange"
              >
                <option value="" disabled>Загрузка моделей...</option>
                <option
                  v-for="model in availableModels"
                  :key="model.name"
                  :value="model.name"
                >
                  {{ model.name }}
                  <span v-if="model.size">
                    ({{ formatFileSize(model.size) }})
                  </span>
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <button
                @click="loadModels"
                class="btn btn-outline-primary btn-sm mt-4"
                :disabled="modelsLoading"
              >
                <i :class="modelsLoading ? 'fas fa-spinner fa-spin' : 'fas fa-sync-alt'"></i>
                Обновить список моделей
              </button>
              <button
                @click="showAdvancedSettings = !showAdvancedSettings"
                class="btn btn-outline-secondary btn-sm mt-4 ms-2"
                title="Расширенные настройки"
              >
                <i class="fas fa-cog"></i>
                Настройки
              </button>
              <div v-if="modelsError" class="text-danger mt-2 small">
                <i class="fas fa-exclamation-triangle"></i>
                {{ modelsError }}
              </div>
            </div>
          </div>
          
          <!-- Расширенные настройки -->
          <div v-if="showAdvancedSettings" class="advanced-settings mt-3 p-3 border rounded bg-light">
            <h6 class="mb-3">
              <i class="fas fa-sliders-h"></i>
              Расширенные параметры модели
            </h6>
            
            <div class="row">
              <!-- Температура -->
              <div class="col-md-4 mb-3">
                <label for="temperature" class="form-label">
                  Температура ({{ modelParams.temperature }})
                  <i class="fas fa-info-circle text-muted"
                     title="Контролирует случайность ответов. Низкие значения (0.1-0.3) - более точные ответы, высокие (0.7-1.0) - более креативные"></i>
                </label>
                <input
                  type="range"
                  id="temperature"
                  v-model.number="modelParams.temperature"
                  min="0"
                  max="2"
                  step="0.1"
                  class="form-range"
                >
                <small class="text-muted">0 (точный) - 2 (креативный)</small>
              </div>
              
              <!-- Top P -->
              <div class="col-md-4 mb-3">
                <label for="topP" class="form-label">
                  Top P ({{ modelParams.top_p }})
                  <i class="fas fa-info-circle text-muted"
                     title="Контролирует разнообразие ответов через nucleus sampling"></i>
                </label>
                <input
                  type="range"
                  id="topP"
                  v-model.number="modelParams.top_p"
                  min="0"
                  max="1"
                  step="0.05"
                  class="form-range"
                >
                <small class="text-muted">0 (узкий выбор) - 1 (широкий выбор)</small>
              </div>
              
              <!-- Max Tokens -->
              <div class="col-md-4 mb-3">
                <label for="maxTokens" class="form-label">
                  Макс. токенов ({{ modelParams.max_tokens }})
                  <i class="fas fa-info-circle text-muted"
                     title="Максимальная длина ответа в токенах"></i>
                </label>
                <input
                  type="number"
                  id="maxTokens"
                  v-model.number="modelParams.max_tokens"
                  min="100"
                  max="4000"
                  step="100"
                  class="form-control"
                >
                <small class="text-muted">100 - 4000 токенов</small>
              </div>
            </div>
            
            <div class="row">
              <!-- Размер контекста истории -->
              <div class="col-md-6 mb-3">
                <label for="contextSize" class="form-label">
                  Размер контекста истории ({{ modelParams.context_size }})
                  <i class="fas fa-info-circle text-muted"
                     title="Количество предыдущих сообщений для контекста"></i>
                </label>
                <input
                  type="number"
                  id="contextSize"
                  v-model.number="modelParams.context_size"
                  min="0"
                  max="20"
                  step="1"
                  class="form-control"
                >
                <small class="text-muted">0 (без истории) - 20 сообщений</small>
              </div>
              
              <!-- Использовать системный контекст -->
              <div class="col-md-6 mb-3">
                <label class="form-label">
                  Системный контекст
                  <i class="fas fa-info-circle text-muted"
                     title="Включать информацию о параметрах системы в запрос"></i>
                </label>
                <div class="form-check form-switch">
                  <input
                    type="checkbox"
                    id="useSystemContext"
                    v-model="modelParams.use_system_context"
                    class="form-check-input"
                  >
                  <label class="form-check-label" for="useSystemContext">
                    {{ modelParams.use_system_context ? 'Включен' : 'Выключен' }}
                  </label>
                </div>
              </div>
            </div>
            
            <!-- Системный промпт -->
            <div class="mb-3">
              <label for="systemPrompt" class="form-label">
                Системный промпт
                <i class="fas fa-info-circle text-muted"
                   title="Инструкции для модели о том, как она должна себя вести"></i>
              </label>
              <textarea
                id="systemPrompt"
                v-model="modelParams.system_prompt"
                class="form-control"
                rows="3"
                placeholder="Введите системный промпт или оставьте пустым для использования по умолчанию"
              ></textarea>
              <small class="text-muted">Оставьте пустым для использования промпта по умолчанию</small>
            </div>

            <!-- Ollama URL -->
            <div class="mb-3">
              <label for="ollamaUrl" class="form-label">
                <i class="fas fa-link"></i>
                Ollama URL
                <i class="fas fa-info-circle text-muted"
                   title="URL сервера Ollama для подключения к моделям"></i>
              </label>
              <div class="input-group">
                <input
                  type="url"
                  id="ollamaUrl"
                  v-model="ollamaUrl"
                  class="form-control"
                  placeholder="http://localhost:11434"
                >
                <button
                  @click="loadOllamaUrl"
                  class="btn btn-outline-secondary"
                  type="button"
                  :disabled="loadingOllamaUrl"
                  title="Загрузить текущий URL"
                >
                  <i :class="loadingOllamaUrl ? 'fas fa-spinner fa-spin' : 'fas fa-download'"></i>
                </button>
                <button
                  @click="saveOllamaUrl"
                  class="btn btn-outline-primary"
                  type="button"
                  :disabled="loadingOllamaUrl || !ollamaUrl"
                  title="Сохранить URL"
                >
                  <i class="fas fa-save"></i>
                </button>
              </div>
              <small class="text-muted">
                URL сервера Ollama (по умолчанию: http://localhost:11434)
                <span v-if="ollamaUrlStatus" :class="ollamaUrlStatus.type === 'success' ? 'text-success' : 'text-danger'">
                  - {{ ollamaUrlStatus.message }}
                </span>
              </small>
            </div>
            
            <!-- Кнопки управления -->
            <div class="d-flex gap-2">
              <button
                @click="resetToDefaults"
                class="btn btn-sm btn-outline-secondary"
              >
                <i class="fas fa-undo"></i>
                Сбросить по умолчанию
              </button>
              <button
                @click="saveSettings"
                class="btn btn-sm btn-success"
              >
                <i class="fas fa-save"></i>
                Сохранить настройки
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Область сообщений -->
      <div class="chat-messages" ref="chatMessages">
        <div v-if="messages.length === 0" class="no-messages">
          <div class="text-center text-muted p-4">
            <i class="fas fa-robot fa-3x mb-3"></i>
            <p>Начните диалог, задав вопрос о ваших данных</p>
            <small>Примеры вопросов:</small>
            <ul class="list-unstyled mt-2">
              <li>• Какие параметры связаны с категорией "Конфигурация"?</li>
              <li>• Покажи последние комментарии пользователей</li>
              <li>• Какие системные опции нужно настроить?</li>
            </ul>
          </div>
        </div>

        <div v-for="(message, index) in messages" :key="index" class="message-row">
          <div class="message" :class="message.role">
            <div class="message-header">
              <!-- <div class="message-avatar">
                <i :class="message.role === 'user' ? 'fas fa-user' : 'fas fa-robot'"></i>
              </div> -->
              <div class="message-meta">
              <div v-if="message.role === 'user'" class="message-role">
                <span class="icon-wrapper text-success"><i class="fas fa-user"></i> Вы </span>
                <span class="message-time"> {{ formatTime(message.timestamp) }}</span>
              <div class="icon-wrapper text-success">{{ message.content }}</div>
              </div>
              <div v-else class="message-role">
                <span class="icon-wrapper text-warning"><i class="fas fa-robot"></i> Ассистент </span>
                <span class="message-time"> {{ formatTime(message.timestamp) }}</span>
              <div class="icon-wrapper text-warning">{{ message.content }}</div>
              </div>
            </div>
            </div>
            <!-- <div class="message-content">
              <div v-if="message.type === 'text'">{{ message.content }}</div>
              <div v-else-if="message.type === 'error'" class="text-danger">
                <i class="fas fa-exclamation-triangle"></i>
                {{ message.content }}
              </div>
              <div v-else-if="message.type === 'loading'" class="loading-message">
                <i class="fas fa-spinner fa-spin"></i>
                {{ message.content }}
              </div>
              <div v-else-if="message.type === 'file'" class="file-message">
                <i class="fas fa-file"></i>
                {{ message.content }}
                <small class="text-muted">({{ message.filename }})</small>
              </div>
            </div> -->
          </div>
        </div>
      </div>

      <!-- Поле ввода -->
      <div class="chat-input-container">
        <!-- История вопросов -->
        <div v-if="questionHistory.length > 0" class="mb-2">
          <label for="questionHistory" class="form-label small text-muted">
            <i class="fas fa-history"></i>
            История вопросов:
          </label>
          <select
            id="questionHistory"
            v-model="selectedHistoryQuestion"
            @change="onHistoryQuestionSelect"
            class="form-control form-control-sm"
          >
            <option value="">Выберите из истории...</option>
            <option
              v-for="(question, index) in questionHistory"
              :key="index"
              :value="question"
            >
              {{ question.length > 80 ? question.substring(0, 80) + '...' : question }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <input
            type="text"
            v-model="currentMessage"
            @keyup.enter="sendMessage"
            placeholder="Введите ваш вопрос..."
            class="form-control"
            :disabled="loading"
          >
          <div class="input-group-append">
            <button
              @click="sendMessage"
              class="btn btn-primary"
              :disabled="loading || !currentMessage.trim()"
              title="Отправить"
            >
              <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane'"></i>
            </button>
          </div>
        </div>

        <!-- Кнопка загрузки файла -->
        <div class="mt-2">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileUpload"
            accept=".txt,.pdf,.doc,.docx"
            style="display: none;"
          >
          <button
            @click="$refs.fileInput.click()"
            class="btn btn-outline-secondary btn-sm"
            :disabled="loading"
            title="Загрузить файл для контекста"
          >
            <i class="fas fa-upload"></i>
            Прикрепить файл
          </button>
          <small v-if="uploadedFile" class="text-muted ms-2">
            Выбран файл: {{ uploadedFile.name }}
          </small>
        </div>
      </div>

      <!-- Ошибки -->
      <div v-if="error" class="alert alert-danger mt-3">
        <i class="fas fa-exclamation-triangle"></i>
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatRAG',
  data() {
    return {
      currentMessage: '',
      messages: [],
      loading: false,
      error: null,
      uploadedFile: null,
      chatHistory: [],
      availableModels: [],
      selectedModel: '',
      modelsLoading: false,
      modelsError: null,
      showAdvancedSettings: false,
      questionHistory: [],
      selectedHistoryQuestion: '',
      modelParams: {
        temperature: 0.7,
        top_p: 0.9,
        max_tokens: 1000,
        context_size: 10,
        use_system_context: true,
        system_prompt: ''
      },
      defaultParams: {
        temperature: 0.7,
        top_p: 0.9,
        max_tokens: 1000,
        context_size: 10,
        use_system_context: true,
        system_prompt: ''
      },
      ollamaUrl: '',
      loadingOllamaUrl: false,
      ollamaUrlStatus: null
    };
  },
  mounted() {
    // Загружаем историю чата из localStorage
    this.loadChatHistory();
    // Загружаем список моделей при инициализации
    this.loadModels();
    // Загружаем сохраненные настройки
    this.loadSettings();
    // Загружаем историю вопросов
    this.loadQuestionHistory();
    // Загружаем URL Ollama
    this.loadOllamaUrl();
  },
  methods: {
    async sendMessage() {
      if (!this.currentMessage.trim() || this.loading) return;

      const userMessage = this.currentMessage.trim();
      this.currentMessage = '';

      // Сохраняем вопрос в историю СРАЗУ после отправки
      this.saveQuestionToHistory(userMessage);

      // Проверяем выбранную модель
      if (!this.selectedModel) {
        this.error = 'Пожалуйста, выберите модель для диалога';
        return;
      }

      // Добавляем сообщение пользователя
      const userMsg = {
        role: 'user',
        type: 'text',
        content: userMessage,
        timestamp: new Date()
      };
      this.messages.push(userMsg);

      // Добавляем индикатор загрузки
      const loadingMsg = {
        role: 'assistant',
        type: 'loading',
        content: `Обрабатываю ваш вопрос моделью ${this.selectedModel}...`,
        timestamp: new Date()
      };
      this.messages.push(loadingMsg);

      this.loading = true;
      this.error = null;

      try {
        // Подготавливаем данные для отправки
        const requestData = {
          question: userMessage,
          model: this.selectedModel,
          chat_history: this.chatHistory.slice(-this.modelParams.context_size),
          temperature: this.modelParams.temperature,
          top_p: this.modelParams.top_p,
          max_tokens: this.modelParams.max_tokens,
          use_system_context: this.modelParams.use_system_context,
          system_prompt: this.modelParams.system_prompt || null,
          ollama_url: this.ollamaUrl
        };

        const response = await axios.post('/api/chat-rag/', requestData, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        // Удаляем сообщение загрузки
        this.messages.pop();

        if (response.data.answer) {
          const assistantMsg = {
            role: 'assistant',
            type: 'text',
            content: response.data.answer,
            timestamp: new Date()
          };
          this.messages.push(assistantMsg);

          // Добавляем в историю чата
          this.chatHistory.push(userMsg, assistantMsg);
          this.saveChatHistory();
        } else {
          throw new Error('Не получен ответ от сервера');
        }

        // Очищаем загруженный файл после отправки
        this.uploadedFile = null;

      } catch (err) {
        // Удаляем сообщение загрузки
        this.messages.pop();

        const errorMsg = {
          role: 'assistant',
          type: 'error',
          content: err.response?.data?.error || 'Ошибка обработки запроса',
          timestamp: new Date()
        };
        this.messages.push(errorMsg);
        this.error = err.response?.data?.error || 'Ошибка обработки запроса';
      } finally {
        this.loading = false;
        
        // Прокручиваем к последнему сообщению
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Проверяем размер файла (макс 10MB)
        if (file.size > 10 * 1024 * 1024) {
          this.error = 'Размер файла не должен превышать 10MB';
          return;
        }

        // Проверяем тип файла
        const allowedTypes = ['text/plain', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(txt|pdf|doc|docx)$/i)) {
          this.error = 'Поддерживаются только файлы: txt, pdf, doc, docx';
          return;
        }

        this.uploadedFile = file;
        this.error = null;

        // Показываем информацию о файле в чате
        const fileMsg = {
          role: 'user',
          type: 'file',
          content: 'Загружен файл для анализа',
          filename: file.name,
          timestamp: new Date()
        };
        this.messages.push(fileMsg);
      }
    },

    scrollToBottom() {
      const chatContainer = this.$refs.chatMessages;
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    },

    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    saveChatHistory() {
      try {
        localStorage.setItem('chatRAG_history', JSON.stringify(this.chatHistory.slice(-20)));
      } catch (e) {
        console.warn('Не удалось сохранить историю чата:', e);
      }
    },

    loadChatHistory() {
      try {
        const saved = localStorage.getItem('chatRAG_history');
        if (saved) {
          this.chatHistory = JSON.parse(saved);
        }
      } catch (e) {
        console.warn('Не удалось загрузить историю чата:', e);
      }
    },

    clearHistory() {
      this.chatHistory = [];
      localStorage.removeItem('chatRAG_history');
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

    async loadModels() {
      this.modelsLoading = true;
      this.modelsError = null;

      try {
        const response = await axios.get('/api/chat-rag/', {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (response.data.models) {
          this.availableModels = response.data.models;
          
          // Пытаемся восстановить сохраненную модель
          const savedModel = this.loadSelectedModel();
          
          // Проверяем, есть ли сохраненная модель в списке доступных
          if (savedModel && this.availableModels.some(m => m.name === savedModel)) {
            this.selectedModel = savedModel;
          } else if (!this.selectedModel && this.availableModels.length > 0) {
            // Если сохраненной модели нет или она недоступна, выбираем первую
            this.selectedModel = this.availableModels[0].name;
            this.saveSelectedModel();
          }
        } else {
          throw new Error('Не получен список моделей');
        }

      } catch (err) {
        this.modelsError = err.response?.data?.error || 'Ошибка загрузки списка моделей';
        this.availableModels = [];
        console.error('Error loading models:', err);
      } finally {
        this.modelsLoading = false;
      }
    },

    onModelChange() {
      // Сохраняем выбранную модель
      this.saveSelectedModel();
      
      // Очищаем историю чата при смене модели (но НЕ историю вопросов)
      this.messages = [];
      this.chatHistory = [];
      this.clearHistory();
    },

    onHistoryQuestionSelect() {
      if (this.selectedHistoryQuestion) {
        this.currentMessage = this.selectedHistoryQuestion;
        this.selectedHistoryQuestion = '';
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    resetToDefaults() {
      this.modelParams = { ...this.defaultParams };
      this.saveSettings();
    },

    saveSettings() {
      try {
        localStorage.setItem('chatRAG_settings', JSON.stringify(this.modelParams));
        // Показываем уведомление об успешном сохранении
        this.error = null;
      } catch (e) {
        console.warn('Не удалось сохранить настройки:', e);
        this.error = 'Не удалось сохранить настройки';
      }
    },

    loadSettings() {
      try {
        const saved = localStorage.getItem('chatRAG_settings');
        if (saved) {
          this.modelParams = { ...this.defaultParams, ...JSON.parse(saved) };
        }
      } catch (e) {
        console.warn('Не удалось загрузить настройки:', e);
      }
    },

    saveSelectedModel() {
      try {
        if (this.selectedModel) {
          localStorage.setItem('chatRAG_selectedModel', this.selectedModel);
        }
      } catch (e) {
        console.warn('Не удалось сохранить выбранную модель:', e);
      }
    },

    loadSelectedModel() {
      try {
        return localStorage.getItem('chatRAG_selectedModel');
      } catch (e) {
        console.warn('Не удалось загрузить выбранную модель:', e);
        return null;
      }
    },

    saveQuestionToHistory(question) {
      try {
        // Проверяем, нет ли уже такого вопроса в истории
        if (!this.questionHistory.includes(question)) {
          // Добавляем в начало массива
          this.questionHistory.unshift(question);
          
          // Ограничиваем историю 50 вопросами
          if (this.questionHistory.length > 50) {
            this.questionHistory = this.questionHistory.slice(0, 50);
          }
          
          // Сохраняем в localStorage
          localStorage.setItem('chatRAG_questionHistory', JSON.stringify(this.questionHistory));
        }
      } catch (e) {
        console.warn('Не удалось сохранить вопрос в историю:', e);
      }
    },

    loadQuestionHistory() {
      try {
        const saved = localStorage.getItem('chatRAG_questionHistory');
        if (saved) {
          this.questionHistory = JSON.parse(saved);
        }
      } catch (e) {
        console.warn('Не удалось загрузить историю вопросов:', e);
        this.questionHistory = [];
      }
    },

    async loadOllamaUrl() {
      this.loadingOllamaUrl = true;
      this.ollamaUrlStatus = null;

      try {
        const response = await axios.get('/api/chat-rag/ollama-url/', {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        if (response.data.ollama_url) {
          this.ollamaUrl = response.data.ollama_url;
        } else {
          // Если URL не получен от сервера, используем значение по умолчанию
          this.ollamaUrl = this.ollamaUrl || 'http://localhost:11434';
        }

      } catch (err) {
        console.warn('Не удалось загрузить URL Ollama:', err);
        // Устанавливаем значение по умолчанию при ошибке
        this.ollamaUrl = this.ollamaUrl || 'http://localhost:11434';
        this.ollamaUrlStatus = {
          type: 'warning',
          message: 'Используется URL по умолчанию'
        };
      } finally {
        this.loadingOllamaUrl = false;
      }
    },

    async saveOllamaUrl() {
      if (!this.ollamaUrl.trim()) {
        this.ollamaUrlStatus = {
          type: 'error',
          message: 'URL не может быть пустым'
        };
        return;
      }

      // Проверяем формат URL
      try {
        new URL(this.ollamaUrl);
      } catch (e) {
        this.ollamaUrlStatus = {
          type: 'error',
          message: 'Неверный формат URL'
        };
        return;
      }

      this.loadingOllamaUrl = true;
      this.ollamaUrlStatus = null;

      try {
        const response = await axios.post('/api/chat-rag/ollama-url/', {
          ollama_url: this.ollamaUrl
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });

        this.ollamaUrlStatus = {
          type: 'success',
          message: 'URL успешно сохранен'
        };

        // Очищаем статус через 3 секунды
        setTimeout(() => {
          this.ollamaUrlStatus = null;
        }, 3000);

      } catch (err) {
        this.ollamaUrlStatus = {
          type: 'error',
          message: err.response?.data?.error || 'Ошибка сохранения URL'
        };
      } finally {
        this.loadingOllamaUrl = false;
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  flex-shrink: 0;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  background-color: #f8f9fa;
  border-radius: 0.375rem 0.375rem 0 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  min-height: 400px;
  max-height: 500px;
  background-color: #ffffff;
}

.message-row {
  margin-bottom: 1rem;
}

.message {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message.user {
  margin-left: auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 1rem 1rem 0.25rem 1rem;
  border-left: 5px solid #4c51bf;
  box-shadow:
    0 4px 6px rgba(102, 126, 234, 0.25),
    0 1px 3px rgba(102, 126, 234, 0.15);
}

.message.assistant {
  margin-right: auto;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  color: #2d3748;
  border: 1px solid #e2e8f0;
  border-radius: 1rem 1rem 1rem 0.25rem;
  border-left: 5px solid #38a169;
  box-shadow:
    0 4px 6px rgba(160, 174, 192, 0.25),
    0 1px 3px rgba(160, 174, 192, 0.15);
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}

.message-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  font-size: 0.75rem;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, #5a67d8 0%, #4c51bf 100%);
  color: white;
  box-shadow:
    0 3px 6px rgba(90, 103, 216, 0.4),
    0 1px 3px rgba(90, 103, 216, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.message.assistant .message-avatar {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
  box-shadow:
    0 3px 6px rgba(72, 187, 120, 0.4),
    0 1px 3px rgba(72, 187, 120, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

/* Дополнительные стили для улучшения визуального разделения */
.message.user .message-role {
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message.user .message-time {
  color: rgba(255, 255, 255, 0.75);
  font-weight: 500;
}

.message.assistant .message-role {
  color: #2d3748;
  font-weight: 600;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.8);
}

.message.assistant .message-time {
  color: #4a5568;
  font-weight: 500;
}

/* Эффект при наведении с учетом цветового разделения */
.message.user:hover {
  transform: translateY(-2px);
  box-shadow:
    0 6px 12px rgba(102, 126, 234, 0.3),
    0 2px 4px rgba(102, 126, 234, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message.assistant:hover {
  transform: translateY(-2px);
  box-shadow:
    0 6px 12px rgba(160, 174, 192, 0.3),
    0 2px 4px rgba(160, 174, 192, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Разделитель между сообщениями для лучшего визуального разделения */
.message-row {
  position: relative;
}

.message-row:not(:last-child)::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
  opacity: 0.3;
}

.message-row:has(.message.user):not(:last-child)::after {
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
}

.message-row:has(.message.assistant):not(:last-child)::after {
  background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.2), transparent);
}

/* Стили для сообщений об ошибках */
.message.assistant .text-danger {
  background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
  padding: 0.75rem;
  border-radius: 0.5rem;
  border-left: 4px solid #f56565;
  color: #742a2a;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(245, 101, 101, 0.2);
}

.message.assistant .loading-message {
  background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
  padding: 0.75rem;
  border-radius: 0.5rem;
  border-left: 4px solid #38b2ac;
  color: #234e52;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(56, 178, 172, 0.2);
}

.message.user .file-message {
  background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%);
  padding: 0.75rem;
  border-radius: 0.5rem;
  border-left: 4px solid #ed8936;
  color: #7c2d12;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(237, 137, 54, 0.2);
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.message-role {
  font-weight: 600;
}

.message-time {
  opacity: 0.7;
  font-size: 0.75rem;
}

.message-content {
  line-height: 1.5;
}

.loading-message {
  color: #6c757d;
  font-style: italic;
}

.file-message {
  background-color: #e9ecef;
  padding: 0.5rem;
  border-radius: 0.25rem;
  border-left: 3px solid #007bff;
}

.no-messages {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
}

.chat-input-container {
  flex-shrink: 0;
  padding: 1rem;
  border-top: 1px solid #dee2e6;
  background-color: #f8f9fa;
  border-radius: 0 0 0.375rem 0.375rem;
}

.input-group {
  margin-bottom: 0.5rem;
}

.btn:disabled {
  cursor: not-allowed;
}

.text-muted {
  color: #6c757d !important;
}

/* Стили для прокрутки */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .container {
    height: 90vh;
  }
  
  .message {
    max-width: 95%;
  }
  
  .chat-messages {
    padding: 0.5rem;
    max-height: 60vh;
  }
  
  .chat-input-container {
    padding: 0.75rem;
  }
}
</style>