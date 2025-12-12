"""
Утилиты для работы с Oracle JDBC
Предоставляет универсальные функции для подключения к Oracle и выполнения SQL запросов
Пример вызова:

"""

import jpype
import jpype.imports
from jpype.types import *
from django.core.management.base import BaseCommand


class OracleJDBCUtil:
    """Утилита для работы с Oracle через JDBC"""
    
    def __init__(self, jar_path='appmsw/java/ojdbc6.jar', connect_id=None):
        """
        Инициализация утилиты Oracle JDBC
        
        Args:
            jar_path (str): Путь к JAR файлу драйвера Oracle
            connect_id (int): ID подключения из модели DbConnection (если указан, параметры берутся из БД)
        """
        self.jar_path = jar_path
        self.connect_id = connect_id
        self.connection = None
        self.statement = None
        self.result_set = None
        
        # Запуск JVM если еще не запущена
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[self.jar_path])
    
    def connect(self, url=None, username=None, password=None, connect_id=None):
        """
        Подключение к Oracle database
        
        Args:
            url (str): JDBC URL для подключения
            username (str): Имя пользователя Oracle
            password (str): Пароль пользователя Oracle
            connect_id (int): ID подключения из модели DbConnection (если указан, параметры берутся из БД)
            
        Returns:
            bool: True если подключение успешно, False иначе
        """
        try:
            # Импорт классов JDBC
            from java.sql import DriverManager, SQLException
            from java.lang import Class
            
            # Если указан connect_id, загружаем параметры из базы данных
            if connect_id:
                from appmsw.models import DbConnection
                
                try:
                    db_conn = DbConnection.objects.get(id=connect_id, database_type='oracle', is_active=True)
                    url = db_conn.connection_string
                    username = db_conn.username
                    password = db_conn.password
                except DbConnection.DoesNotExist:
                    print(f"Подключение с ID {connect_id} не найдено или не является активным подключением к Oracle")
                    return False
            elif self.connect_id:
                # Если connect_id передан в конструкторе, используем его
                from appmsw.models import DbConnection
                
                try:
                    db_conn = DbConnection.objects.get(id=self.connect_id, database_type='oracle', is_active=True)
                    url = db_conn.connection_string
                    username = db_conn.username
                    password = db_conn.password
                except DbConnection.DoesNotExist:
                    print(f"Подключение с ID {self.connect_id} не найдено или не является активным подключением к Oracle")
                    return False
            
            # Загрузка драйвера Oracle
            Class.forName("oracle.jdbc.driver.OracleDriver")
            
            # Подключение к базе данных
            self.connection = DriverManager.getConnection(url, username, password)
            return True
            
        except Exception as e:
            print(f"Ошибка подключения к Oracle: {str(e)}")
            return False
    
    def execute_query(self, sql_query):
        """
        Выполнение SQL запроса и получение результатов
        
        Args:
            sql_query (str): SQL запрос для выполнения
            
        Returns:
            list: Список результатов запроса (каждый результат - список значений строки)
                  None в случае ошибки
        """
        if not self.connection:
            print("Нет активного подключения к базе данных")
            return None
        
        try:
            # Создание statement и выполнение запроса
            self.statement = self.connection.createStatement()
            self.result_set = self.statement.executeQuery(sql_query)
            
            # Получение метаданных результата
            columns_count = self.result_set.getMetaData().getColumnCount()
            results = []
            
            # Обработка результатов
            while self.result_set.next():
                row = []
                for i in range(1, columns_count + 1):
                    value = self.result_set.getObject(i)
                    # Преобразуем java объекты в Python строки
                    if value is not None:
                        if hasattr(value, '__str__'):
                            row.append(str(value))
                        else:
                            row.append(repr(value))
                    else:
                        row.append(None)
                results.append(row)
            
            return results
            
        except Exception as e:
            print(f"Ошибка выполнения запроса: {str(e)}")
            return None
    
    def execute_update(self, sql_query):
        """
        Выполнение SQL запроса обновления (INSERT, UPDATE, DELETE)
        
        Args:
            sql_query (str): SQL запрос для выполнения
            
        Returns:
            int: Количество измененных строк или -1 в случае ошибки
        """
        if not self.connection:
            print("Нет активного подключения к базе данных")
            return -1
        
        try:
            # Создание statement и выполнение запроса
            self.statement = self.connection.createStatement()
            result = self.statement.executeUpdate(sql_query)
            return result
            
        except Exception as e:
            print(f"Ошибка выполнения обновления: {str(e)}")
            return -1
    
    def get_column_names(self):
        """
        Получение имен колонок последнего выполненного запроса
        
        Returns:
            list: Список имен колонок или None в случае ошибки
        """
        if not self.result_set:
            return None
        
        try:
            metadata = self.result_set.getMetaData()
            column_count = metadata.getColumnCount()
            column_names = []
            
            for i in range(1, column_count + 1):
                column_name = metadata.getColumnName(i)
                column_names.append(column_name)
            
            return column_names
            
        except Exception as e:
            print(f"Ошибка получения имен колонок: {str(e)}")
            return None
    
    def close(self):
        """Закрытие всех ресурсов и отключение от базы данных"""
        try:
            if self.result_set:
                self.result_set.close()
            if self.statement:
                self.statement.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Ошибка при закрытии ресурсов: {str(e)}")
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие ресурсов при выходе из контекста"""
        self.close()


def execute_oracle_query(url, username, password, sql_query):
    """
    Удобная функция для выполнения SQL запроса к Oracle
    
    Args:
        url (str): JDBC URL для подключения к Oracle
        username (str): Имя пользователя Oracle
        password (str): Пароль пользователя Oracle
        sql_query (str): SQL запрос для выполнения
        
    Returns:
        tuple: (column_names, results) где:
               - column_names: список имен колонок
               - results: список результатов запроса
               Возвращает (None, None) в случае ошибки
    """
    with OracleJDBCUtil() as oracle_util:
        if not oracle_util.connect(url=url, username=username, password=password):
            return None, None
        
        results = oracle_util.execute_query(sql_query)
        column_names = oracle_util.get_column_names()
        
        return column_names, results


def test_oracle_connection(url, username, password):
    """
    Функция для тестирования подключения к Oracle
    
    Args:
        url (str): JDBC URL для подключения к Oracle
        username (str): Имя пользователя Oracle
        password (str): Пароль пользователя Oracle
        
    Returns:
        bool: True если подключение успешно, False иначе
    """
    with OracleJDBCUtil() as oracle_util:
        return oracle_util.connect(url=url, username=username, password=password)


# Пример использования
if __name__ == "__main__":
    # Настройки подключения по умолчанию
    DEFAULT_URL = 'jdbc:oracle:thin:@localhost:1521:xe'
    DEFAULT_USERNAME = 'your_username'
    DEFAULT_PASSWORD = 'your_password'
    DEFAULT_SQL = 'SELECT 1 FROM DUAL'
    
    # Пример использования
    print("Тестирование подключения к Oracle...")
    
    if test_oracle_connection(url=DEFAULT_URL, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        print("Подключение к Oracle успешно!")
        
        # Выполнение тестового запроса
        column_names, results = execute_oracle_query(
            url=DEFAULT_URL,
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
            sql_query=DEFAULT_SQL
        )
        
        if results:
            print("Результаты запроса:")
            if column_names:
                print("\t".join(column_names))
            for row in results:
                print("\t".join(str(val) for val in row))
        else:
            print("Запрос не вернул результатов")
    else:
        print("Ошибка подключения к Oracle")