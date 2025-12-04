<template>
  <div>
    <div class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1 class="m-0">
              {{ currentTabInfo.name }}
              <span class="ml-2">
                <i
                  class="fas fa-user-circle text-info"
                  data-toggle="tooltip"
                  data-placement="bottom"
                  :title="getUserTooltipText()"
                  style="cursor: help; font-size: 0.9em;"
                ></i>
              </span>
            </h1>
          </div>
        </div>
      </div>
    </div>

    <section class="content">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <div class="card card-primary card-outline">
              <div class="card-body">
                <!-- Отображаем только выбранную вкладку -->
                <div v-if="currentTabInfo">
                  <component :is="currentTabInfo.component" />
                </div>
                <div v-else class="alert alert-warning">
                  Неверный ID вкладки. Доступные вкладки: Параметры (params), Системные опции (sysoptions), Комментарии (comments), Запросы (queries), Диалог (chats), Брокер сообщений – RabbitMQ (rabbitmq), Отчеты КРУ (reportskru), Отчеты УЗ (reportsuz), УАС ЕАИСТ (uas), УСПП ЕАИСТ (uspp), ЦБ РФ (cbrf), ЦУ КГХ (cukgh), АСУР СМЭВ (asur), Служба 112 (mvk112), ГИС ЖКХ (giszhkh), SuperSet (supersets), AirFlow (airflow).
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Params from './views/Params.vue'
import SysOptions from './views/SysOptions.vue'
import Comments from './views/Comments.vue'
import DbQueries from './views/DbQueries.vue'
import ChatRAG from './views/ChatRAG.vue'
import RabbitMQ from './views/RabbitMQ.vue'
import Airflow from './views/Airflow.vue'
import SuperSet from './views/SuperSet.vue'
import GisZhkh from './views/GisZhkh.vue'
import Mvk112 from './views/Mvk112.vue'
import Asur from './views/Asur.vue'
import CUKgh from './views/CUKgh.vue'
import CBRF from './views/CBRF.vue'
import USPP from './views/USPP.vue'
import UAS from './views/UAS.vue'
import ReportsUZ from './views/ReportsUZ.vue'
import ReportsKRU from './views/ReportsKRU.vue'

export default {
  name: 'App',
  components: {
    Params,
    SysOptions,
    Comments,
    DbQueries,
    ChatRAG,
    RabbitMQ,
    Airflow,
    SuperSet,
    GisZhkh,
    Mvk112,
    Asur,
    CUKgh,
    CBRF,
    USPP,
    UAS,
    ReportsUZ,
    ReportsKRU
  },
  data() {
    return {
      // Сопоставление ID вкладок с их названиями
      tabs: [
        {
          id: 'params',
          name: 'Параметры',
          component: 'Params'
        },
        {
          id: 'sysoptions',
          name: 'Системные опции',
          component: 'SysOptions'
        },
        {
          id: 'comments',
          name: 'Комментарии',
          component: 'Comments'
        },
        {
          id: 'queries',
          name: 'Запросы',
          component: 'DbQueries'
        },
        {
          id: 'chats',
          name: 'Диалог',
          component: 'ChatRAG'
        },
        {
          id: 'rabbitmq',
          name: 'Брокер сообщений – RabbitMQ',
          component: 'RabbitMQ'
        },
        {
          id: 'reportskru',
          name: 'Отчеты КРУ',
          component: 'ReportsKRU'
        },
        {
          id: 'reportsuz',
          name: 'Отчеты УЗ',
          component: 'ReportsUZ'
        },
        {
          id: 'uas',
          name: 'УАС ЕАИСТ',
          component: 'UAS'
        },
        {
          id: 'uspp',
          name: 'УСПП ЕАИСТ',
          component: 'USPP'
        },
        {
          id: 'cbrf',
          name: 'ЦБ РФ',
          component: 'CBRF'
        },
        {
          id: 'cukgh',
          name: 'ЦУ КГХ',
          component: 'CUKgh'
        },
        {
          id: 'asur',
          name: 'АСУР СМЭВ',
          component: 'Asur'
        },
        {
          id: 'mvk112',
          name: 'Служба 112',
          component: 'Mvk112'
        },
        {
          id: 'giszhkh',
          name: 'ГИС ЖКХ',
          component: 'GisZhkh'
        },
        {
          id: 'supersets',
          name: 'SuperSet',
          component: 'SuperSet'
        },
        {
          id: 'airflow',
          name: 'AirFlow',
          component: 'Airflow'
        }
      ],
      selectedTabId: null
    }
  },
  computed: {
    currentTabInfo() {
      if (!this.selectedTabId) return null
      return this.tabs.find(tab => tab.id === this.selectedTabId) || null
    }
  },
  mounted() {
    // Получаем selectedTabId из глобальной переменной или используем значение по умолчанию
    this.selectedTabId = window.currentTabId || 1
    console.log('Vue app mounted with tab ID:', this.selectedTabId)
    this.initTooltips()
  },
  methods: {
    getUserTooltipText() {
      const currentUser = this.$currentUser
      if (!currentUser) {
        return 'Пользователь не аутентифицирован'
      }
      
      let roles = []
      if (currentUser.is_superuser) roles.push('Суперпользователь')
      if (currentUser.is_staff) roles.push('Администратор')
      if (!roles.length) roles.push('Пользователь')
      
      return `Текущий пользователь: ${currentUser.username}\n` +
             `Email: ${currentUser.email || 'не указан'}\n` +
             `Роли: ${roles.join(', ')}\n` +
             `ID: ${currentUser.id}`
    },
    initTooltips() {
      // Инициализируем Bootstrap tooltips
      this.$nextTick(() => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new window.bootstrap.Tooltip(tooltipTriggerEl)
        })
      })
    }
  }
}
</script>

<style scoped>
</style>