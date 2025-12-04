import jaydebeapi

# Путь к драйверу JDBC
driver_path = 'appmsw/java/postgresql-42.3.1.jar'

# Параметры подключения
url = 'jdbc:postgresql://192.168.0.106:5433/postgres'  # Замените на ваш URL базы данных
# url = 'jdbc:postgresql://172.24.86.249:5434/airflow'  # Замените на ваш URL базы данных
user = 'postgres'  # Замените на ваше имя пользователя
# user = 'airflow'  # Замените на ваше имя пользователя
password = 'postgres'  # Замените на ваш пароль
# password = 'airflow'  # Замените на ваш пароль
if 1==1:
    url = 'jdbc:postgresql://172.24.86.249:5434/airflow'  # Замените на ваш URL базы данных
    user = 'airflow'  # Замените на ваше имя пользователя
    password = 'airflow'  # Замените на ваш пароль



try:
    # Подключение к базе данных через JDBC
    conn = jaydebeapi.connect('org.postgresql.Driver', url, [user, password], driver_path)

    # Создание курсора
    curs = conn.cursor()

    # Выполнение простого запроса
    curs.execute('SELECT 1 as test_column')

    # Получение и вывод результата
    result = curs.fetchall()
    print('Тест успешен:', result)

    # Закрытие курсора и соединения
    curs.close()
    conn.close()

except Exception as e:
    print('Ошибка:', e)