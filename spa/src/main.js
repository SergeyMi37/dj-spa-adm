import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'admin-lte/dist/css/adminlte.min.css'
import 'admin-lte/dist/js/adminlte.min.js'
import '@fortawesome/fontawesome-free/css/all.min.css'

// Функция для создания и монтирования Vue приложения
function mountVueApp(tabId) {
    console.log('Mounting Vue application...', 'Tab ID:', tabId);
    
    // Устанавливаем глобальную переменную для передачи tabId в Vue компонент
    if (tabId) {
        window.currentTabId = tabId;
    }
    
    // Создаем глобальный объект для хранения информации о пользователе
    const app = createApp(App)
    app.config.globalProperties.$currentUser = window.currentUser || null

    // Добавляем метод для получения CSRF токена
    app.config.globalProperties.getCookie = function(name) {
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
    }

    app.use(router).mount('#app')
    console.log('Vue application mounted successfully');
}

// Делаем функцию глобально доступной
window.mountVueApp = mountVueApp;

// Если DOM уже загружен, монтируем приложение
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountVueApp);
} else {
    // DOM уже загружен
    mountVueApp();
}