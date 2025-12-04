

## dj-spa-adm

![](https://raw.githubusercontent.com/SergeyMi37/dj-spa-adm/master/doc/icons/AdminLTELogo.png)

Application tools for use Django AdminLte and SPA.

<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/SergeyMi37/dj-spa-adm">

## What's new

Implemented support for connecting to IRIS via the JDBC library.

![](https://raw.githubusercontent.com/SergeyMi37/dj-spa-adm/master/doc/icons/logo-apptools.png)

## Start the app in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`)

```bash
$ git clone https://github.com/SergeyMi37/dj-spa-adm.git
$ cd dj-spa-adm
```

> 👉 **Step 2** - Start the APP in `Docker`

Копировать файл в .env из env.sample и изменить переменные при необходимости
Пропишите ваш реальный IP адрес в переменную CSRF_TRUSTED_ORIGINS

```bash
$ docker-compose up -d
```

В докере создадутся супер-пользователи adm и developer с паролем demo

Visit `http://localhost:5085` in your browser. The app should be up & running.

После этого пароль нужно сменить

<br />


## Manual Build 

> 👉 Download the code  

```bash
$ git clone https://github.com/SergeyMi37/dj-spa-adm.git
$ cd dj-spa-adm
```

<br />

> 👉 Install modules via `VENV`  

Create .env file in root directory and copy-paste this or just run `cp env_sample .env`, :

```
DEBUG=True
SECRET_KEY=gix%#3&%giwv8f0+%r946en7z&d@9*rc$sl0qoq7z&d@9*rc$sl0qoql56xr%bh^w2mj
CSRF_TRUSTED_ORIGINS=http://real-you-IP:5085
DJANGO_SUPERUSER_PASSWORD=demo

APPMSW_PARAM_NANE=Basic
APPMSW_LOGO_TITLE=MsW-Title
APPMSW_LOGO_FOOTER=MsW-Footer

# Connection string for iris via Nativ Python libs
#APPMSW_IRIS_URL=iris://superuser:SYS@iris:1972/USER

# Connection string for iris via JDBC libs
APPMSW_IRIS_URL=jdbc://superuser:SYS@iris:1972/USER

```bash
# virtualenv env
  # Linux/Mac
python3 -m venv env-lin
source env-lin/bin/activate
  # Windows
python -m venv env-win
source env-win/Scripts/activate

pip install -r requirements-win.txt

pip install appmsw/api/intersystems_irispython-3.2.0-py3-none-any.whl
python -m pip install --upgrade pip
python manage.py makemigrations  # если появилась новая модель
python manage.py migrate         # если есть изменения в моделях
python manage.py createsuperuser # adm, developer # если новая установка
python manage.py loaddata db-init-param.json      # если новая установка
cd spa && npm install && cd ..                    # если новая установка
python manage.py rebuild_spa    # если изменился код Vue компонент пересобрать SPA
python manage.py collectstatic --noinput  # для запуска статики через ngingx
cp -r static/spa staticfiles/             # для запуска через ngingx
python manage.py runserver    # запустить сервер для разработки на порту 8000
python manage.py runserver 0.0.0.0:8080 # если запустить для всех и на порту не 8000

```

At this point, the app runs at
`http://127.0.0.1:8000/` - Интерфейс Django с кампонентами AdminLte
`http://127.0.0.1:8000/api/docs/` - Swagger v.3 к моделям Django
`http://127.0.0.1:8000/my-spa-page/` - Vue.js SPA с AdminLTE темой

## Vue.js SPA (Single Page Application)

Проект включает Vue.js SPA, интегрированную в Django приложение с использованием AdminLTE темы.

### Доступные страницы SPA:
- `http://127.0.0.1:8000/my-spa-page/` - Главная страница
- `http://127.0.0.1:8000/my-spa-page/params` - Список параметров
- `http://127.0.0.1:8000/my-spa-page/sysoptions` - Системные опции
- `http://127.0.0.1:8000/my-spa-page/comments` - Комментарии
- `http://127.0.0.1:8000/my-spa-page/about` - О программе

### Установка и обновление SPA

> 👉 **Установка Node.js и npm**

Перед работой с SPA необходимо установить Node.js и npm:

**Для Windows:**
1. Скачайте Node.js с официального сайта: https://nodejs.org/
2. Запустите установщик и следуйте инструкциям
3. Перезапустите командную строку
4. Проверьте установку:
```cmd
node --version
npm --version
```

**Для Linux (Ubuntu/Debian):**
```bash
# Обновите пакетный индекс
sudo apt update

# Установите Node.js и npm
sudo apt install nodejs npm

# Или установите последнюю версию через NodeSource
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Проверьте установку
node --version
npm --version
```

**Для Linux (CentOS/RHEL):**
```bash
# Установите Node.js и npm
sudo yum install nodejs npm

# Или через NodeSource для более новых версий
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install nodejs npm

# Проверьте установку
node --version
npm --version
```

> 👉 **Установка зависимостей SPA**

```bash
$ cd spa && npm install && cd ..
```

**Важно**: Если возникает ошибка "vite не является внутренней или внешней командой", убедитесь, что зависимости установлены локально в папке `spa`. При необходимости выполните принудительную установку:

```bash
$ cd spa && npm install --force && cd ..
```

> 👉 **Сборка SPA для продакшена**

```bash
$ cd spa && npm run build && cd ..
```

> 👉 **Сборка SPA для разработки**

```bash
$ cd spa && npm run build -- --mode development  && cd ..
```

> 👉 **Запуск сервера разработки SPA**

```bash
$ cd spa && npm run dev  && cd ..
```

> 👉 **Обновление статических файлов Django**

После сборки SPA необходимо обновить статические файлы Django:

```bash
$ python manage.py collectstatic --noinput
$ cp -r static/spa staticfiles/
```

### Структура SPA

```
spa/
├── src/
│   ├── views/           # Компоненты страниц
│   │   ├── Home.vue     # Главная страница
│   │   ├── Params.vue   # Параметры
│   │   ├── SysOptions.vue # Системные опции
│   │   ├── Comments.vue # Комментарии
│   │   └── About.vue    # О программе
│   ├── router/
│   │   └── index.js     # Настройка маршрутизации
│   ├── App.vue          # Основной компонент
│   └── main.js          # Точка входа
├── vite.config.js       # Конфигурация Vite
└── package.json         # Зависимости
```

### Особенности интеграции

- **CSRF защита**: Все API запросы защищены CSRF токенами
- **Совместное использование шаблонизаторов**: Django и Vue работают вместе
- **Автоматическая загрузка**: Данные загружаются при открытии страниц
- **Обработка ошибок**: Показываются сообщения об ошибках загрузки

## Утилиты командной строки

```
#  Пересборка SPA:
python manage.py rebuild_spa

#  Статистика всех моделей Django:
python manage.py model_stats

#  Детальная информация о конкретной модели:
python manage.py check_model appmsw.param

#  Экспорт модели в файл json:
python manage.py model_import --model Param --file test.json --format json --import 0
# или
python manage.py model_import --model Param --file test.json --format json

#  Экспорт модели в файл csv (по умолчанию):
python manage.py model_import --model sysoption --file sysotiom.csv --format csv

#  Импорт модели из файла json в режиме --dry-run - сухой запуск, без реального импорта:
python manage.py model_import --model SysOption --file sysotion.json --format json --import 1 --dry-run

#  Импорт модели из файла json:
python manage.py model_import --model SysOption --file sysotion.json --format json --import 1

```