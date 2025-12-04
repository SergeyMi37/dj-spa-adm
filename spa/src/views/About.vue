<template>
  <div class="row">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">О программе</h3>
        </div>
        <div class="card-body">
          <p>Это Vue.js SPA интегрированная в Django проект с использованием AdminLTE темы.</p>
          <p>Технологии:</p>
          <ul>
            <li>Vue.js 3</li>
            <li>Vue Router 4</li>
            <li>AdminLTE 3</li>
            <li>Vite</li>
            <li>Django</li>
          </ul>
          <p>Особенности интеграции:</p>
          <ul>
            <li>CSRF защита для AJAX запросов</li>
            <li>Совместное использование шаблонизаторов Django и Vue</li>
            <li>Оптимизированная сборка статических файлов</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>