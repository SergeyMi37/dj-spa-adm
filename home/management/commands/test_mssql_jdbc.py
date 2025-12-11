from django.core.management.base import BaseCommand
import jpype
import jpype.imports
from jpype.types import *

class Command(BaseCommand):
    help = 'Тест выполнения SQL в MS SQL Server по JDBC'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='jdbc:sqlserver://localhost:1433;databaseName=master;encrypt=false;trustServerCertificate=true', help='JDBC URL для подключения к MS SQL Server')
        parser.add_argument('--username', type=str, default='sa', help='Имя пользователя MS SQL Server')
        parser.add_argument('--password', type=str, default='your_password', help='Пароль пользователя MS SQL Server')
        parser.add_argument('--sql', type=str, default='SELECT 1', help='SQL-запрос для выполнения (по умолчанию: SELECT 1)')

    def handle(self, *args, **options):
        # Путь к драйверу MS SQL Server
        jar_path = 'appmsw/java/sqljdbc42.jar'

        # Запуск JVM с указанием пути к драйверу
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[jar_path])

        try:
            # Импорт классов JDBC
            from java.sql import DriverManager, SQLException
            from java.lang import Class

            # Загрузка драйвера MS SQL Server
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")

            # Отключение SSL/TLS шифрования
            from java.lang import System
            System.setProperty("javax.net.ssl.trustStore", "")
            System.setProperty("javax.net.ssl.trustStoreType", "Windows-ROOT")
            System.setProperty("java.security.enabledAlgorithms", "TLSv1,TLSv1.1,TLSv1.2")
            System.setProperty("https.protocols", "TLSv1,TLSv1.1,TLSv1.2")

            # Подключение к базе данных
            url = options['url']
            username = options['username']
            password = options['password']

            self.stdout.write(f'Подключение к MS SQL Server: {url}')
            conn = DriverManager.getConnection(url, username, password)
            self.stdout.write('Соединение с MS SQL Server установлено')

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