#  python manage.py test_oracle_jdbc_cid --connect-id 3 --sql "SELECT banner FROM v\$version"

from django.core.management.base import BaseCommand
from appmsw.jdbc_util import OracleJDBCUtil, execute_oracle_query


class Command(BaseCommand):
    help = 'Тест выполнения SQL в Oracle по JDBC с использованием OracleJDBCUtil'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='jdbc:oracle:thin:@localhost:1521:xe',
                            help='JDBC URL для подключения к Oracle')
        parser.add_argument('--username', type=str, default='your_username',
                            help='Имя пользователя Oracle')
        parser.add_argument('--password', type=str, default='your_password',
                            help='Пароль пользователя Oracle')
        parser.add_argument('--connect-id', type=int,
                            help='ID подключения из базы данных (если указан, используются параметры из БД)')
        parser.add_argument('--sql', type=str, default='SELECT 1 FROM DUAL',
                            help='SQL-запрос для выполнения (по умолчанию: SELECT 1 FROM DUAL)')
        parser.add_argument('--jar-path', type=str, default='appmsw/java/ojdbc6.jar',
                            help='Путь к JAR файлу драйвера Oracle')

    def handle(self, *args, **options):
        url = options['url']
        username = options['username']
        password = options['password']
        connect_id = options['connect_id']
        sql_query = options['sql']
        jar_path = options['jar_path']

        try:
            # Используем OracleJDBCUtil для подключения и выполнения запроса
            with OracleJDBCUtil(jar_path=jar_path, connect_id=connect_id) as oracle_util:
                if connect_id:
                    self.stdout.write(f'Тестирование подключения к Oracle с использованием параметров из БД (ID: {connect_id})')
                    if oracle_util.connect(connect_id=connect_id):
                        self.stdout.write(self.style.SUCCESS('Соединение с Oracle установлено'))
                    else:
                        self.stdout.write(self.style.ERROR('Не удалось подключиться к Oracle'))
                        return
                else:
                    self.stdout.write(f'Тестирование подключения к Oracle: {url}')
                    if oracle_util.connect(url=url, username=username, password=password):
                        self.stdout.write(self.style.SUCCESS('Соединение с Oracle установлено'))
                    else:
                        self.stdout.write(self.style.ERROR('Не удалось подключиться к Oracle'))
                        return

                self.stdout.write(f'Выполнение запроса: {sql_query}')
                results = oracle_util.execute_query(sql_query=sql_query)

                if results:
                    self.stdout.write('Результаты запроса получены')
                    column_names = oracle_util.get_column_names()
                    if column_names:
                        self.stdout.write('Имена колонок:')
                        self.stdout.write('\t'.join(str(col) for col in column_names))

                    self.stdout.write('Вывод строк результата:')
                    for idx, row in enumerate(results):
                        self.stdout.write(f'Строка {idx + 1}:')
                        
                        # Преобразуем java объекты в Python строки
                        converted_row = []
                        for j, val in enumerate(row):
                            self.stdout.write(f'  Колонка {j + 1}: Тип={type(val)}, Значение={val}')
                            
                            if val is not None:
                                if hasattr(val, '__str__'):
                                    converted_row.append(str(val))
                                else:
                                    converted_row.append(repr(val))
                            else:
                                converted_row.append('')
                        
                        # Отладочная информация перед объединением
                        self.stdout.write(f'  Преобразованная строка: {converted_row}')
                        self.stdout.write(f'  Типы элементов: {[type(x) for x in converted_row]}')
                        
                        try:
                            result_str = '\t'.join(converted_row)
                            self.stdout.write(result_str)
                        except TypeError as e:
                            self.stdout.write(self.style.ERROR(f'Ошибка при объединении строки: {e}'))
                            # Резервный способ вывода
                            for val in converted_row:
                                self.stdout.write(str(val) + '\t', ending='')
                            self.stdout.write('')  # Перевод строки
                else:
                    self.stdout.write('Запрос не вернул результатов')

                self.stdout.write(self.style.SUCCESS('Тестирование завершено успешно'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {str(e)}'))