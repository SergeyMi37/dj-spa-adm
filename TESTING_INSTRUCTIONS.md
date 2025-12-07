# Инструкция по запуску тестов для DbConnection и SysOption

Данный документ описывает процесс запуска тестов для моделей `DbConnection` и `SysOption`, включая CRUD операции и тестирование документации Swagger.

## Структура тестов

Тесты разделены на следующие категории:

1. `DbConnectionCRUDTestCase` - Тестирование CRUD операций для DbConnection
2. `DbConnectionPermissionsTestCase` - Тестирование прав доступа для DbConnection
3. `DbConnectionSwaggerDocumentationTestCase` - Тестирование документации Swagger для DbConnection
4. `SysOptionCRUDTestCase` - Тестирование CRUD операций для SysOption
5. `SysOptionPermissionsTestCase` - Тестирование прав доступа для SysOption
6. `SysOptionSwaggerDocumentationTestCase` - Тестирование документации Swagger для SysOption

## Требования

- Python 3.8+
- Django
- djangorestframework
- drf-spectacular (для Swagger документации)
- pytest-django (опционально)

## Запуск тестов

### 1. Запуск всех тестов для приложения appmsw

```bash
python manage.py test appmsw
```

### 2. Запуск только тестов DbConnection

```bash
python manage.py test appmsw.tests.DbConnectionCRUDTestCase
```

### 3. Запуск только тестов SysOption

```bash
python manage.py test appmsw.tests.SysOptionCRUDTestCase
```

### 4. Запуск конкретного теста

```bash
python manage.py test appmsw.tests.SysOptionCRUDTestCase.test_create_sys_option
```

### 5. Запуск с детальным выводом

```bash
python manage.py test appmsw --verbosity=2
```

### 6. Запуск с покрытием кода

```bash
pip install coverage
coverage run --source='.' manage.py test appmsw
coverage report
coverage html  # для генерации HTML отчета
```

## Использование pytest (если установлен)

### 1. Запуск всех тестов

```bash
pytest
```

### 2. Запуск тестов для конкретного файла

```bash
pytest appmsw/tests.py
```

### 3. Запуск тестов с конкретным тегом (если настроены)

```bash
pytest -k "sys_option"
```

## Описание тестов

### DbConnectionCRUDTestCase

- `test_create_db_connection` - Проверяет создание нового подключения к БД
- `test_get_db_connection_list` - Проверяет получение списка подключений
- `test_get_single_db_connection` - Проверяет получение одного подключения
- `test_update_db_connection` - Проверяет полное обновление подключения
- `test_partial_update_db_connection` - Проверяет частичное обновление подключения
- `test_delete_db_connection` - Проверяет удаление подключения

### DbConnectionPermissionsTestCase

- `test_user_can_access_own_connection` - Проверяет, что пользователь может получить доступ к своим подключениям
- `test_user_cannot_access_other_user_connection` - Проверяет, что пользователь не может получить доступ к чужим подключениям
- `test_unauthenticated_access_denied` - Проверяет, что неавторизованный доступ запрещен

### DbConnectionSwaggerDocumentationTestCase

- `test_swagger_schema_available` - Проверяет доступность схемы Swagger
- `test_swagger_ui_available` - Проверяет доступность интерфейса Swagger
- `test_db_connection_in_swagger_schema` - Проверяет, что DbConnection API присутствует в схеме Swagger

### SysOptionCRUDTestCase

- `test_create_sys_option` - Проверяет создание новой системной опции
- `test_get_sys_option_list` - Проверяет получение списка системных опций
- `test_get_single_sys_option` - Проверяет получение одной системной опции
- `test_update_sys_option` - Проверяет полное обновление системной опции
- `test_partial_update_sys_option` - Проверяет частичное обновление системной опции
- `test_delete_sys_option` - Проверяет удаление системной опции

### SysOptionPermissionsTestCase

- `test_user_can_access_own_option` - Проверяет, что пользователь может получить доступ к своим системным опциям
- `test_user_cannot_access_other_user_option` - Проверяет, что пользователь не может получить доступ к чужим системным опциям
- `test_unauthenticated_access_denied` - Проверяет, что неавторизованный доступ запрещен

### SysOptionSwaggerDocumentationTestCase

- `test_swagger_schema_available` - Проверяет доступность схемы Swagger
- `test_swagger_ui_available` - Проверяет доступность интерфейса Swagger
- `test_sys_option_in_swagger_schema` - Проверяет, что SysOption API присутствует в схеме Swagger

## Примеры успешного выполнения тестов

После запуска тестов вы должны увидеть результаты в формате:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................  # точки представляют успешные тесты
----------------------------------------------------------------------
Ran 23 tests in 0.789s

OK
Destroying test database for alias 'default'...
```

## Возможные проблемы и решения

1. **Ошибки аутентификации**: Убедитесь, что тестовые пользователи создаются корректно
2. **Проблемы с подключением к БД**: Тесты используют встроенную в Django поддержку тестовых БД
3. **Ошибки импорта**: Убедитесь, что все зависимости установлены

## Дополнительные параметры запуска

```bash
# Запуск тестов без миграций БД
python manage.py test appmsw --keepdb

# Запуск тестов с сохранением тестовой БД
python manage.py test appmsw --debug-mode

# Запуск тестов с ограничением по времени
python manage.py test appmsw --parallel