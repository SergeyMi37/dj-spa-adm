<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2><i class="fas fa-map-marker-alt"></i> ГИС ЖКХ</h2>
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
              Государственная информационная система ЖКХ
            </h5>
            <p class="card-text">
              ГИС ЖКХ - это единая федеральная централизованная информационная система, 
              предназначенная для обеспечения сбора, обработки, хранения, предоставления, 
              обмена и использования информации в сфере жилищно-коммунального хозяйства.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="row">
      <!-- Панель навигации ГИС ЖКХ -->
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
              @click="activeSection = 'houses'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'houses' }]"
            >
              <i class="fas fa-building me-2"></i>
              Многоквартирные дома
            </button>
            <button 
              @click="activeSection = 'utilities'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'utilities' }]"
            >
              <i class="fas fa-tools me-2"></i>
              Коммунальные услуги
            </button>
            <button 
              @click="activeSection = 'payments'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'payments' }]"
            >
              <i class="fas fa-money-bill me-2"></i>
              Платежи
            </button>
            <button 
              @click="activeSection = 'repairs'"
              :class="['list-group-item', 'list-group-item-action', { 'active': activeSection === 'repairs' }]"
            >
              <i class="fas fa-wrench me-2"></i>
              Ремонт и содержание
            </button>
          </div>
        </div>
      </div>

      <!-- Основная область контента -->
      <div class="col-md-9">
        <!-- Раздел Многоквартирные дома -->
        <div v-if="activeSection === 'houses'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-building"></i>
              Многоквартирные дома
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="input-group" style="max-width: 300px;">
                <input 
                  v-model="searchQuery"
                  type="text" 
                  class="form-control form-control-sm" 
                  placeholder="Поиск по адресу..."
                >
                <div class="input-group-append">
                  <button class="btn btn-outline-secondary btn-sm" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <button 
                @click="addNewHouse"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Добавить дом
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Адрес</th>
                    <th>Управляющая организация</th>
                    <th>Год постройки</th>
                    <th>Этажность</th>
                    <th>Квартир</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="house in filteredHouses" :key="house.id">
                    <td>{{ house.address }}</td>
                    <td>
                      <small>{{ house.management_company }}</small>
                    </td>
                    <td>{{ house.construction_year }}</td>
                    <td>{{ house.floors }}</td>
                    <td>{{ house.apartments }}</td>
                    <td>
                      <span 
                        :class="['badge', house.status === 'active' ? 'bg-success' : 'bg-warning']"
                      >
                        {{ house.status === 'active' ? 'Активный' : 'Неактивный' }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewHouse(house.id)"
                          class="btn btn-outline-primary"
                          title="Просмотр"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="editHouse(house.id)"
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

            <div v-if="filteredHouses.length === 0" class="text-center py-4">
              <i class="fas fa-building fa-3x text-muted mb-3"></i>
              <p class="text-muted">Дома не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Коммунальные услуги -->
        <div v-if="activeSection === 'utilities'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-tools"></i>
              Коммунальные услуги
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3" v-for="service in utilityServices" :key="service.id">
                <div class="card h-100">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i :class="getServiceIcon(service.type)"></i>
                      {{ service.name }}
                    </h6>
                    <p class="card-text">
                      <small class="text-muted">{{ service.description }}</small>
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                      <span 
                        :class="['badge', service.status === 'active' ? 'bg-success' : 'bg-danger']"
                      >
                        {{ service.status === 'active' ? 'Подключен' : 'Отключен' }}
                      </span>
                      <small class="text-muted">{{ service.houses_count }} домов</small>
                    </div>
                    <div class="mt-2">
                      <small class="text-muted">
                        Тариф: {{ service.tariff }} руб./{{ service.unit }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="utilityServices.length === 0" class="text-center py-4">
              <i class="fas fa-tools fa-3x text-muted mb-3"></i>
              <p class="text-muted">Услуги не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Платежи -->
        <div v-if="activeSection === 'payments'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-money-bill"></i>
              Платежи
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div>
                <select v-model="paymentFilter" class="form-control form-control-sm" style="width: 150px; display: inline-block;">
                  <option value="all">Все платежи</option>
                  <option value="paid">Оплаченные</option>
                  <option value="pending">Ожидающие</option>
                  <option value="overdue">Просроченные</option>
                </select>
              </div>
              <button 
                @click="addPayment"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Новый платеж
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Дата</th>
                    <th>Адрес</th>
                    <th>Услуга</th>
                    <th>Сумма</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="payment in filteredPayments" :key="payment.id">
                    <td>
                      <small>{{ formatDate(payment.date) }}</small>
                    </td>
                    <td>{{ payment.address }}</td>
                    <td>{{ payment.service }}</td>
                    <td class="text-right">
                      <strong>{{ payment.amount.toLocaleString('ru-RU') }} ₽</strong>
                    </td>
                    <td>
                      <span 
                        :class="getPaymentStatusClass(payment.status)"
                        class="badge"
                      >
                        {{ getPaymentStatusText(payment.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          v-if="payment.status === 'pending'"
                          @click="markAsPaid(payment.id)"
                          class="btn btn-outline-success"
                          title="Отметить оплаченным"
                        >
                          <i class="fas fa-check"></i>
                        </button>
                        <button 
                          @click="viewPayment(payment.id)"
                          class="btn btn-outline-primary"
                          title="Подробнее"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredPayments.length === 0" class="text-center py-4">
              <i class="fas fa-money-bill fa-3x text-muted mb-3"></i>
              <p class="text-muted">Платежи не найдены</p>
            </div>
          </div>
        </div>

        <!-- Раздел Ремонт и содержание -->
        <div v-if="activeSection === 'repairs'" class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-wrench"></i>
              Ремонт и содержание
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
              <div class="btn-group" role="group">
                <button 
                  @click="repairFilter = 'all'"
                  :class="['btn', 'btn-sm', repairFilter === 'all' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Все
                </button>
                <button 
                  @click="repairFilter = 'planned'"
                  :class="['btn', 'btn-sm', repairFilter === 'planned' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Запланированные
                </button>
                <button 
                  @click="repairFilter = 'in_progress'"
                  :class="['btn', 'btn-sm', repairFilter === 'in_progress' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  В процессе
                </button>
                <button 
                  @click="repairFilter = 'completed'"
                  :class="['btn', 'btn-sm', repairFilter === 'completed' ? 'btn-primary' : 'btn-outline-primary']"
                >
                  Завершенные
                </button>
              </div>
              <button 
                @click="scheduleRepair"
                class="btn btn-success btn-sm"
              >
                <i class="fas fa-plus"></i>
                Запланировать
              </button>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>Дата</th>
                    <th>Адрес</th>
                    <th>Вид работ</th>
                    <th>Стоимость</th>
                    <th>Исполнитель</th>
                    <th>Статус</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="repair in filteredRepairs" :key="repair.id">
                    <td>
                      <small>{{ formatDate(repair.scheduled_date) }}</small>
                    </td>
                    <td>{{ repair.address }}</td>
                    <td>{{ repair.work_type }}</td>
                    <td class="text-right">
                      {{ repair.cost.toLocaleString('ru-RU') }} ₽
                    </td>
                    <td>
                      <small>{{ repair.contractor }}</small>
                    </td>
                    <td>
                      <span 
                        :class="getRepairStatusClass(repair.status)"
                        class="badge"
                      >
                        {{ getRepairStatusText(repair.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button 
                          @click="viewRepair(repair.id)"
                          class="btn btn-outline-primary"
                          title="Подробнее"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          v-if="repair.status === 'planned'"
                          @click="startRepair(repair.id)"
                          class="btn btn-outline-success"
                          title="Начать работы"
                        >
                          <i class="fas fa-play"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="filteredRepairs.length === 0" class="text-center py-4">
              <i class="fas fa-wrench fa-3x text-muted mb-3"></i>
              <p class="text-muted">Ремонтные работы не найдены</p>
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
  name: 'GisZhkh',
  data() {
    return {
      loading: false,
      error: null,
      activeSection: 'houses',
      searchQuery: '',
      paymentFilter: 'all',
      repairFilter: 'all',
      
      // Данные многоквартирных домов
      houses: [
        {
          id: 1,
          address: 'г. Москва, ул. Тверская, д. 15',
          management_company: 'ООО "УправДом"',
          construction_year: 1985,
          floors: 9,
          apartments: 144,
          status: 'active'
        },
        {
          id: 2,
          address: 'г. Москва, пр-т Мира, д. 42',
          management_company: 'ООО "ЖилСервис"',
          construction_year: 1992,
          floors: 12,
          apartments: 192,
          status: 'active'
        },
        {
          id: 3,
          address: 'г. Москва, ул. Ленина, д. 7',
          management_company: 'ООО "Городской сервис"',
          construction_year: 1978,
          floors: 5,
          apartments: 80,
          status: 'inactive'
        }
      ],

      // Данные коммунальных услуг
      utilityServices: [
        {
          id: 1,
          name: 'Холодное водоснабжение',
          type: 'water',
          description: 'Подача холодной воды',
          status: 'active',
          houses_count: 145,
          tariff: 35.78,
          unit: 'м³'
        },
        {
          id: 2,
          name: 'Горячее водоснабжение',
          type: 'hot_water',
          description: 'Подача горячей воды',
          status: 'active',
          houses_count: 142,
          tariff: 198.25,
          unit: 'м³'
        },
        {
          id: 3,
          name: 'Электроснабжение',
          type: 'electricity',
          description: 'Подача электроэнергии',
          status: 'active',
          houses_count: 145,
          tariff: 5.15,
          unit: 'кВт·ч'
        },
        {
          id: 4,
          name: 'Газоснабжение',
          type: 'gas',
          description: 'Подача природного газа',
          status: 'active',
          houses_count: 138,
          tariff: 6.16,
          unit: 'м³'
        },
        {
          id: 5,
          name: 'Теплоснабжение',
          type: 'heating',
          description: 'Отопление помещений',
          status: 'active',
          houses_count: 145,
          tariff: 1944.62,
          unit: 'Гкал'
        }
      ],

      // Данные платежей
      payments: [
        {
          id: 1,
          date: new Date('2024-01-15'),
          address: 'г. Москва, ул. Тверская, д. 15, кв. 45',
          service: 'Холодное водоснабжение',
          amount: 1250.50,
          status: 'paid'
        },
        {
          id: 2,
          date: new Date('2024-01-14'),
          address: 'г. Москва, пр-т Мира, д. 42, кв. 123',
          service: 'Электроснабжение',
          amount: 890.25,
          status: 'pending'
        },
        {
          id: 3,
          date: new Date('2024-01-10'),
          address: 'г. Москва, ул. Ленина, д. 7, кв. 8',
          service: 'Теплоснабжение',
          amount: 2150.75,
          status: 'overdue'
        }
      ],

      // Данные ремонтных работ
      repairs: [
        {
          id: 1,
          scheduled_date: new Date('2024-02-01'),
          address: 'г. Москва, ул. Тверская, д. 15',
          work_type: 'Замена кровли',
          cost: 250000,
          contractor: 'ООО "Кровельщик"',
          status: 'planned'
        },
        {
          id: 2,
          scheduled_date: new Date('2024-01-20'),
          address: 'г. Москва, пр-т Мира, д. 42',
          work_type: 'Ремонт лифта',
          cost: 150000,
          contractor: 'ООО "ЛифтСервис"',
          status: 'in_progress'
        },
        {
          id: 3,
          scheduled_date: new Date('2024-01-05'),
          address: 'г. Москва, ул. Ленина, д. 7',
          work_type: 'Покраска подъезда',
          cost: 45000,
          contractor: 'ИП Петров',
          status: 'completed'
        }
      ]
    };
  },
  computed: {
    filteredHouses() {
      if (!this.searchQuery) return this.houses;
      return this.houses.filter(house => 
        house.address.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    filteredPayments() {
      if (this.paymentFilter === 'all') return this.payments;
      return this.payments.filter(payment => payment.status === this.paymentFilter);
    },

    filteredRepairs() {
      if (this.repairFilter === 'all') return this.repairs;
      return this.repairs.filter(repair => repair.status === this.repairFilter);
    }
  },
  methods: {
    async refreshData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Имитация обновления данных
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('ГИС ЖКХ данные обновлены');
      } catch (err) {
        this.error = 'Ошибка при обновлении данных';
      } finally {
        this.loading = false;
      }
    },

    exportData() {
      // Имитация экспорта данных
      console.log('Экспорт данных ГИС ЖКХ');
      alert('Экспорт данных ГИС ЖКХ (заглушка)');
    },

    addNewHouse() {
      console.log('Добавление нового дома');
      alert('Добавление нового дома (заглушка)');
    },

    viewHouse(houseId) {
      console.log(`Просмотр дома ${houseId}`);
      alert(`Просмотр дома ${houseId} (заглушка)`);
    },

    editHouse(houseId) {
      console.log(`Редактирование дома ${houseId}`);
      alert(`Редактирование дома ${houseId} (заглушка)`);
    },

    getServiceIcon(type) {
      const icons = {
        water: 'fas fa-tint text-primary',
        hot_water: 'fas fa-fire text-danger',
        electricity: 'fas fa-bolt text-warning',
        gas: 'fas fa-gas-pump text-success',
        heating: 'fas fa-thermometer-half text-info'
      };
      return icons[type] || 'fas fa-tools text-secondary';
    },

    addPayment() {
      console.log('Добавление нового платежа');
      alert('Добавление нового платежа (заглушка)');
    },

    markAsPaid(paymentId) {
      const payment = this.payments.find(p => p.id === paymentId);
      if (payment) {
        payment.status = 'paid';
      }
      console.log(`Платеж ${paymentId} отмечен как оплаченный`);
    },

    viewPayment(paymentId) {
      console.log(`Просмотр платежа ${paymentId}`);
      alert(`Просмотр платежа ${paymentId} (заглушка)`);
    },

    getPaymentStatusClass(status) {
      const classes = {
        paid: 'bg-success',
        pending: 'bg-warning',
        overdue: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getPaymentStatusText(status) {
      const texts = {
        paid: 'Оплачен',
        pending: 'Ожидает',
        overdue: 'Просрочен'
      };
      return texts[status] || status;
    },

    scheduleRepair() {
      console.log('Планирование ремонтных работ');
      alert('Планирование ремонтных работ (заглушка)');
    },

    viewRepair(repairId) {
      console.log(`Просмотр ремонта ${repairId}`);
      alert(`Просмотр ремонта ${repairId} (заглушка)`);
    },

    startRepair(repairId) {
      const repair = this.repairs.find(r => r.id === repairId);
      if (repair) {
        repair.status = 'in_progress';
      }
      console.log(`Ремонт ${repairId} начат`);
    },

    getRepairStatusClass(status) {
      const classes = {
        planned: 'bg-info',
        in_progress: 'bg-warning',
        completed: 'bg-success'
      };
      return classes[status] || 'bg-secondary';
    },

    getRepairStatusText(status) {
      const texts = {
        planned: 'Запланирован',
        in_progress: 'В процессе',
        completed: 'Завершен'
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
    console.log('ГИС ЖКХ компонента инициализирована');
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