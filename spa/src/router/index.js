import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Params from '../views/Params.vue'
import SysOptions from '../views/SysOptions.vue'
import Comments from '../views/Comments.vue'
import DbQueries from '../views/DbQueries.vue'
import ChatRAG from '../views/ChatRAG.vue'
import RabbitMQ from '../views/RabbitMQ.vue'
import Airflow from '../views/Airflow.vue'
import SuperSet from '../views/SuperSet.vue'
import GisZhkh from '../views/GisZhkh.vue'
import Mvk112 from '../views/Mvk112.vue'
import Asur from '../views/Asur.vue'
import CUKgh from '../views/CUKgh.vue'
import CBRF from '../views/CBRF.vue'
import USPP from '../views/USPP.vue'
import UAS from '../views/UAS.vue'
import ReportsUZ from '../views/ReportsUZ.vue'
import ReportsKRU from '../views/ReportsKRU.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Главная' }
  },
  {
    path: '/params',
    name: 'Params',
    component: Params,
    meta: { title: 'Параметры' }
  },
  {
    path: '/sysoptions',
    name: 'SysOptions',
    component: SysOptions,
    meta: { title: 'Системные опции' }
  },
  {
    path: '/comments',
    name: 'Comments',
    component: Comments,
    meta: { title: 'Комментарии' }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: { title: 'О программе' }
  },
  {
    path: '/dbqueries',
    name: 'DbQueries',
    component: DbQueries,
    meta: { title: 'Запросы к бд' }
  },
  {
    path: '/chat',
    name: 'ChatRAG',
    component: ChatRAG,
    meta: { title: 'Ассистент' }
  },
  {
    path: '/rabbitmq',
    name: 'RabbitMQ',
    component: RabbitMQ,
    meta: { title: 'Брокер сообщений – RabbitMQ' }
  },
  {
    path: '/airflow',
    name: 'Airflow',
    component: Airflow,
    meta: { title: 'AirFlow' }
  },
  {
    path: '/supersets',
    name: 'SuperSet',
    component: SuperSet,
    meta: { title: 'SuperSet' }
  },
  {
    path: '/giszhkh',
    name: 'GisZhkh',
    component: GisZhkh,
    meta: { title: 'ГИС ЖКХ' }
  },
  {
    path: '/mvk112',
    name: 'Mvk112',
    component: Mvk112,
    meta: { title: 'Служба 112' }
  },
  {
    path: '/asur',
    name: 'Asur',
    component: Asur,
    meta: { title: 'АСУР СМЭВ' }
  },
  {
    path: '/cukgh',
    name: 'CUKgh',
    component: CUKgh,
    meta: { title: 'ЦУ КГХ' }
  },
  {
    path: '/cbrf',
    name: 'CBRF',
    component: CBRF,
    meta: { title: 'ЦБ РФ' }
  },
  {
    path: '/uspp',
    name: 'USPP',
    component: USPP,
    meta: { title: 'УСПП ЕАИСТ' }
  },
  {
    path: '/uas',
    name: 'UAS',
    component: UAS,
    meta: { title: 'УАС ЕАИСТ' }
  },
  {
    path: '/reportsuz',
    name: 'ReportsUZ',
    component: ReportsUZ,
    meta: { title: 'Отчеты УЗ' }
  },
  {
    path: '/reportskru',
    name: 'ReportsKRU',
    component: ReportsKRU,
    meta: { title: 'Отчеты КРУ' }
  }
]

const router = createRouter({
   history: createWebHistory(),
   routes
 })

export default router