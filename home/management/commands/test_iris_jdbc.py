from django.core.management.base import BaseCommand
import jpype
import jpype.imports
from jpype.types import *

class Command(BaseCommand):
    help = 'Тест выполнения SQL в IRIS по JDBC'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='jdbc:IRIS://localhost:1972/USER', help='JDBC URL для подключения к IRIS')
        parser.add_argument('--username', type=str, default='_SYSTEM', help='Имя пользователя IRIS')
        parser.add_argument('--password', type=str, default='SYS', help='Пароль пользователя IRIS')
        parser.add_argument('--sql', type=str, default='SELECT 1', help='SQL-запрос для выполнения (по умолчанию: SELECT 1)')

    def handle(self, *args, **options):
        # Путь к драйверу IRIS
        jar_path = 'appmsw/java/intersystems-jdbc-3.7.1.jar'

        # Запуск JVM с указанием пути к драйверу
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[jar_path])

        try:
            # Импорт классов JDBC
            from java.sql import DriverManager, SQLException
            from java.lang import Class

            # Загрузка драйвера IRIS
            Class.forName("com.intersystems.jdbc.IRISDriver")

            # Подключение к базе данных
            url = options['url']
            username = options['username']
            password = options['password']

            self.stdout.write(f'Подключение к IRIS: {url}')
            conn = DriverManager.getConnection(url, username, password)
            self.stdout.write('Соединение с IRIS установлено')

            # Выполнение указанного SQL-запроса
            sql_query = options['sql']
            self.stdout.write(f'Выполнение запроса: {sql_query}')

            stmt = conn.createStatement()
            rs = stmt.executeQuery(sql_query)

            # Вывод результатов запроса
            columns_count = rs.getMetaData().getColumnCount()
            results_found = False

            while rs.next():
                results_found = True
                row = []
                for i in range(1, columns_count + 1):
                    value = rs.getObject(i)
                    row.append(str(value))
                self.stdout.write('\t'.join(row))

            if not results_found:
                self.stdout.write('Запрос не вернул результатов')

            # Закрытие ресурсов
            rs.close()
            stmt.close()
            conn.close()
            self.stdout.write('Соединение закрыто')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {str(e)}'))
        finally:
            # Остановка JVM
            if jpype.isJVMStarted():
                jpype.shutdownJVM()