# views.py
from rest_framework import viewsets, permissions, status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from appmsw.models import Param, Comment, SysOption, DbConnection
from appmsw.serializers import ParamSerializer, CommentSerializer, SysOptionSerializer, DbConnectionSerializer
from django.db import models

@extend_schema_view(
    list=extend_schema(
        description='Получить список всех параметров',
        summary='Список параметров',
        parameters=[
            OpenApiParameter(
                name='category',
                description='Фильтр по категории',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='public',
                description='Фильтр по публичности',
                required=False,
                type=bool
            )
        ]
    ),
    retrieve=extend_schema(
        description='Получить детальную информацию о параметре',
        summary='Детали параметра'
    ),
    create=extend_schema(
        description='Создать новый параметр',
        summary='Создание параметра',
        examples=[
            OpenApiExample(
                'Пример создания параметра',
                value={
                    'name': 'Название параметра',
                    'category': 'app',
                    'desc': 'Описание параметра',
                    'option': 'Опции',
                    'json': '{"key": "value"}',
                    'value': 'Значение параметра',
                    'public': True
                }
            )
        ]
    ),
    update=extend_schema(
        description='Обновить параметр полностью',
        summary='Полное обновление параметра'
    ),
    partial_update=extend_schema(
        description='Частично обновить параметр',
        summary='Частичное обновление параметра'
    ),
    destroy=extend_schema(
        description='Удалить параметр',
        summary='Удаление параметра'
    )
)
class ParamViewSet(viewsets.ModelViewSet):
    queryset = Param.objects.all()
    serializer_class = ParamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Param.objects.all()
        category = self.request.query_params.get('category')
        public = self.request.query_params.get('public')

        if category:
            queryset = queryset.filter(category=category)
        if public:
            queryset = queryset.filter(public=public.lower() == 'true')

        # Фильтрация по правам пользователя
        user = self.request.user
        if user.is_authenticated:
            # Проверяем права доступа к модели Param
            if user.has_perm('appmsw.view_param'):
                # Показывать публичные параметры и параметры созданные пользователем
                queryset = queryset.filter(
                    models.Q(public=True) | models.Q(user=user)
                )
            else:
                # Если нет прав на просмотр параметров, возвращаем пустой queryset
                queryset = queryset.none()
        else:
            # Для неавторизованных пользователей только публичные параметры
            queryset = queryset.filter(public=True)

        return queryset

@extend_schema_view(
    list=extend_schema(
        description='Получить список комментариев',
        summary='Список комментариев'
    ),
    retrieve=extend_schema(
        description='Получить детальную информацию о комментарии',
        summary='Детали комментария'
    ),
    create=extend_schema(
        description='Создать новый комментарий',
        summary='Создание комментария',
        examples=[
            OpenApiExample(
                'Пример создания комментария',
                value={
                    'text': 'Текст комментария',
                    'param': 1
                }
            )
        ]
    ),
    update=extend_schema(
        description='Обновить комментарий полностью',
        summary='Полное обновление комментария'
    ),
    partial_update=extend_schema(
        description='Частично обновить комментарий',
        summary='Частичное обновление комментария'
    ),
    destroy=extend_schema(
        description='Удалить комментарий',
        summary='Удаление комментария'
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all()
        # Фильтрация по правам пользователя
        user = self.request.user
        if user.is_authenticated:
            # Проверяем права доступа к модели Comment
            if user.has_perm('appmsw.view_comment'):
                # Показывать комментарии пользователя и комментарии к параметрам, которые пользователь может видеть
                user_params = Param.objects.filter(
                    models.Q(public=True) | models.Q(user=user)
                ).values_list('id', flat=True)
                queryset = queryset.filter(
                    models.Q(author=user) | models.Q(param__in=user_params)
                )
            else:
                # Если нет прав на просмотр комментариев, возвращаем пустой queryset
                queryset = queryset.none()
        else:
            # Для неавторизованных пользователей только комментарии к публичным параметрам
            public_params = Param.objects.filter(public=True).values_list('id', flat=True)
            queryset = queryset.filter(param__in=public_params)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@extend_schema_view(
    list=extend_schema(
        description='Получить список всех системных опций',
        summary='Список системных опций',
        parameters=[
            OpenApiParameter(
                name='category',
                description='Фильтр по категории',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='public',
                description='Фильтр по публичности',
                required=False,
                type=bool
            )
        ]
    ),
    retrieve=extend_schema(
        description='Получить детальную информацию о системной опции',
        summary='Детали системной опции'
    ),
    create=extend_schema(
        description='Создать новую системную опцию',
        summary='Создание системной опции',
        examples=[
            OpenApiExample(
                'Пример создания системной опции',
                value={
                    'name': 'Название опции',
                    'category': 'app',
                    'desc': 'Описание опции',
                    'option': 'Опции',
                    'json': '{"key": "value"}',
                    'value': 'Значение опции',
                    'public': True
                }
            )
        ]
    ),
    update=extend_schema(
        description='Обновить системную опцию полностью',
        summary='Полное обновление системной опции'
    ),
    partial_update=extend_schema(
        description='Частично обновить системную опцию',
        summary='Частичное обновление системной опции'
    ),
    destroy=extend_schema(
        description='Удалить системную опцию',
        summary='Удаление системной опции'
    )
)
class SysOptionViewSet(viewsets.ModelViewSet):
    queryset = SysOption.objects.all()
    serializer_class = SysOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = SysOption.objects.all()
        category = self.request.query_params.get('category')
        public = self.request.query_params.get('public')

        if category:
            queryset = queryset.filter(category=category)
        if public:
            queryset = queryset.filter(public=public.lower() == 'true')

        # Фильтрация по правам пользователя
        user = self.request.user
        if user.is_authenticated:
            # Проверяем права доступа к модели SysOption
            if user.has_perm('appmsw.view_sysoption'):
                # Показывать публичные опции и опции созданные пользователем
                queryset = queryset.filter(
                    models.Q(public=True) | models.Q(user=user)
                )
            else:
                # Если нет прав на просмотр системных опций, возвращаем пустой queryset
                queryset = queryset.none()
        else:
            # Для неавторизованных пользователей только публичные опции
            queryset = queryset.filter(public=True)

        return queryset

@extend_schema_view(
    list=extend_schema(
        description='Получить список подключений к БД',
        summary='Список подключений'
    ),
    retrieve=extend_schema(
        description='Получить детальную информацию о подключении',
        summary='Детали подключения'
    ),
    create=extend_schema(
        description='Создать новое подключение к БД',
        summary='Создание подключения',
        examples=[
            OpenApiExample(
                'Пример создания подключения',
                value={
                    'name': 'Основная PostgreSQL БД',
                    'database_type': 'postgresql',
                    'connection_string': 'jdbc:postgresql://localhost:5432/mydb',
                    'username': 'user',
                    'password': 'password',
                    'description': 'Подключение к основной базе данных'
                }
            )
        ]
    ),
    update=extend_schema(
        description='Обновить подключение полностью',
        summary='Полное обновление подключения'
    ),
    partial_update=extend_schema(
        description='Частично обновить подключение',
        summary='Частичное обновление подключения'
    ),
    destroy=extend_schema(
        description='Удалить подключение',
        summary='Удаление подключения'
    )
)
class DbConnectionViewSet(viewsets.ModelViewSet):
    queryset = DbConnection.objects.all()
    serializer_class = DbConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Фильтрация по правам пользователя
        user = self.request.user
        if user.is_authenticated:
            # Показывать подключения пользователя и публичные подключения
            queryset = DbConnection.objects.filter(
                models.Q(user=user) | models.Q(is_active=True)
            )
        else:
            # Для неавторизованных пользователей только активные подключения
            queryset = DbConnection.objects.filter(is_active=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @extend_schema(
        description='Тестирование подключения к базе данных',
        summary='Тест подключения',
        request={
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'connection': {
                            'type': 'object',
                            'properties': {
                                'database_type': {
                                    'type': 'string',
                                    'enum': ['postgresql', 'oracle', 'iris'],
                                    'description': 'Тип базы данных',
                                    'example': 'postgresql'
                                },
                                'connection_string': {
                                    'type': 'string',
                                    'description': 'JDBC строка подключения',
                                    'example': 'jdbc:postgresql://localhost:5432/mydb'
                                },
                                'username': {
                                    'type': 'string',
                                    'description': 'Имя пользователя БД',
                                    'example': 'user'
                                },
                                'password': {
                                    'type': 'string',
                                    'description': 'Пароль пользователя БД',
                                    'example': 'password123'
                                }
                            },
                            'required': ['database_type', 'connection_string', 'username']
                        }
                    },
                    'required': ['connection']
                }
            }
        },
        responses={
            200: {
                'description': 'Результат тестирования подключения',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'success': {'type': 'boolean'},
                                'message': {'type': 'string'},
                                'connection_info': {
                                    'type': 'object',
                                    'properties': {
                                        'type': {'type': 'string'},
                                        'host': {'type': 'string'},
                                        'port': {'type': 'integer'},
                                        'database': {'type': 'string'},
                                        'status': {'type': 'string'},
                                        'jdbc_url': {'type': 'string'}
                                    }
                                },
                                'error': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    )
    @extend_schema(
        description='Тестирование подключения к базе данных',
        summary='Тест подключения',
        request={
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'connection': {
                            'type': 'object',
                            'properties': {
                                'database_type': {
                                    'type': 'string',
                                    'enum': ['postgresql', 'oracle', 'iris'],
                                    'description': 'Тип базы данных',
                                    'example': 'postgresql'
                                },
                                'connection_string': {
                                    'type': 'string',
                                    'description': 'JDBC строка подключения',
                                    'example': 'jdbc:postgresql://localhost:5432/mydb'
                                },
                                'username': {
                                    'type': 'string',
                                    'description': 'Имя пользователя БД',
                                    'example': 'user'
                                },
                                'password': {
                                    'type': 'string',
                                    'description': 'Пароль пользователя БД',
                                    'example': 'password123'
                                }
                            },
                            'required': ['database_type', 'connection_string', 'username']
                        }
                    },
                    'required': ['connection']
                }
            }
        },
        responses={
            200: {
                'description': 'Результат тестирования подключения',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'success': {'type': 'boolean'},
                                'message': {'type': 'string'},
                                'connection_info': {
                                    'type': 'object',
                                    'properties': {
                                        'type': {'type': 'string'},
                                        'host': {'type': 'string'},
                                        'port': {'type': 'integer'},
                                        'database': {'type': 'string'},
                                        'status': {'type': 'string'},
                                        'jdbc_url': {'type': 'string'}
                                    }
                                },
                                'error': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    )
    @action(detail=False, methods=['post'], url_path='test-connection')
    def test_connection(self, request):
        """Тестирование подключения к БД"""
        try:
            connection_data = request.data.get('connection', {})
            
            if not connection_data:
                return JsonResponse({
                    'error': 'Данные подключения не предоставлены'
                }, status=400)
            
            # Валидация данных подключения
            # Поддерживаем как camelCase (от frontend), так и snake_case (backwards compatibility)
            connection_string = (
                connection_data.get('connectionString') or
                connection_data.get('connection_string')
            )
            username = connection_data.get('username')
            password = connection_data.get('password', '')
            database_type = (
                connection_data.get('databaseType') or
                connection_data.get('database_type', 'postgresql')
            )
            
            required_fields = ['connectionString', 'connection_string', 'username']
            if not any(connection_data.get(field) for field in ['connectionString', 'connection_string']) or not username:
                return JsonResponse({
                    'error': 'Поля connectionString/connection_string и username обязательны'
                }, status=400)
            
            if database_type == 'iris':
                view_instance = DbQueryAPIView()
                return view_instance.test_iris_connection(connection_string, username, password)
            else:
                view_instance = DbQueryAPIView()
                return view_instance.test_standard_db_connection(connection_string, username, password, database_type)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка тестирования подключения: {str(e)}'
            }, status=500)

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
import json
import jaydebeapi
import os
from urllib.parse import urlparse
from appmsw.iris import classMethod
from core.settings import IRIS_JARS, POSTGRES_JARS

@never_cache  # Отключает кеширование
@csrf_protect  # CSRF защита
def spa_view(request):
    context = {}
    if request.user.is_authenticated:
        context['current_user'] = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'permissions': list(request.user.get_all_permissions())
        }
    else:
        context['current_user'] = None
    
    return render(request, 'spa_page.html', context)

@extend_schema(
    description='Выполнение SQL запроса к базе данных с поддержкой пагинации',
    summary='Выполнение SQL запроса',
    request={
        'application/json': {
            'schema': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'SQL запрос для выполнения',
                        'example': 'SELECT * FROM appmsw_param LIMIT 10'
                    },
                    'limit': {
                        'type': 'integer',
                        'description': 'Количество записей на странице',
                        'example': 50,
                        'minimum': 1,
                        'maximum': 1000
                    },
                    'offset': {
                        'type': 'integer',
                        'description': 'Смещение (количество пропущенных записей)',
                        'example': 0,
                        'minimum': 0
                    },
                    'connectionId': {
                        'type': 'integer',
                        'description': 'ID сохраненного подключения к внешней БД',
                        'example': 1,
                        'nullable': True
                    },
                    'testConnection': {
                        'type': 'boolean',
                        'description': 'Флаг для тестирования подключения к БД',
                        'example': False
                    },
                    'connection': {
                        'type': 'object',
                        'description': 'Данные подключения для тестирования (используется при testConnection=true)',
                        'properties': {
                            'database_type': {
                                'type': 'string',
                                'enum': ['postgresql', 'oracle', 'iris'],
                                'description': 'Тип базы данных',
                                'example': 'postgresql'
                            },
                            'connection_string': {
                                'type': 'string',
                                'description': 'JDBC строка подключения',
                                'example': 'jdbc:postgresql://localhost:5432/mydb'
                            },
                            'username': {
                                'type': 'string',
                                'description': 'Имя пользователя БД',
                                'example': 'user'
                            },
                            'password': {
                                'type': 'string',
                                'description': 'Пароль пользователя БД',
                                'example': 'password123'
                            }
                        },
                        'required': ['database_type', 'connection_string', 'username']
                    }
                },
                'required': ['query'],
                'examples': {
                    'simple_query': {
                        'summary': 'Простой SELECT запрос',
                        'value': {
                            'query': 'SELECT * FROM appmsw_param LIMIT 10'
                        }
                    },
                    'paginated_query': {
                        'summary': 'Запрос с пагинацией',
                        'value': {
                            'query': 'SELECT * FROM appmsw_param WHERE public = true',
                            'limit': 5,
                            'offset': 10
                        }
                    },
                    'external_connection': {
                        'summary': 'Запрос к внешней БД',
                        'value': {
                            'query': 'SELECT * FROM external_table LIMIT 20',
                            'limit': 20,
                            'offset': 0,
                            'connectionId': 1
                        }
                    },
                    'test_connection': {
                        'summary': 'Тестирование подключения',
                        'value': {
                            'testConnection': True,
                            'connection': {
                                'database_type': 'postgresql',
                                'connection_string': 'jdbc:postgresql://localhost:5432/mydb',
                                'username': 'user',
                                'password': 'password123'
                            }
                        }
                    }
                }
            }
        }
    },
    responses={
        200: {
            'description': 'Успешное выполнение SELECT запроса',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'columns': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Список названий колонок'
                            },
                            'rows': {
                                'type': 'array',
                                'items': {
                                    'type': 'array',
                                    'items': {'type': 'string'}
                                },
                                'description': 'Данные запроса (строки таблицы)'
                            },
                            'pagination': {
                                'type': 'object',
                                'description': 'Информация о пагинации',
                                'properties': {
                                    'total_count': {'type': 'integer'},
                                    'limit': {'type': 'integer'},
                                    'offset': {'type': 'integer'},
                                    'has_next': {'type': 'boolean'},
                                    'has_previous': {'type': 'boolean'},
                                    'current_page': {'type': 'integer'},
                                    'total_pages': {'type': 'integer'}
                                }
                            }
                        }
                    },
                    'example': {
                        'columns': ['id', 'name', 'category'],
                        'rows': [[1, 'param1', 'app'], [2, 'param2', 'system']],
                        'pagination': {
                            'total_count': 100,
                            'limit': 50,
                            'offset': 0,
                            'has_next': True,
                            'has_previous': False,
                            'current_page': 1,
                            'total_pages': 2
                        }
                    }
                }
            }
        },
        201: {
            'description': 'Успешное выполнение команды (не SELECT)',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'affected_rows': {'type': 'integer'}
                        }
                    },
                    'example': {
                        'message': 'Запрос выполнен успешно',
                        'affected_rows': 5
                    }
                }
            }
        },
        400: {
            'description': 'Ошибка валидации данных',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {'type': 'string'}
                        }
                    },
                    'example': {
                        'error': 'Пустой запрос'
                    }
                }
            }
        },
        500: {
            'description': 'Ошибка выполнения SQL запроса',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {'type': 'string'}
                        }
                    },
                    'example': {
                        'error': 'Ошибка выполнения запроса: таблица не найдена'
                    }
                }
            }
        }
    }
)
class DbQueryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Обработка SQL запросов с поддержкой пагинации"""
        try:
            # Проверяем, это ли это тестирование подключения
            test_connection = request.data.get('testConnection', False)
            if test_connection:
                return self.test_connection(request)
            
            query = request.data.get('query', '').strip()
            limit = request.data.get('limit', 50)  # По умолчанию 50 записей
            offset = request.data.get('offset', 0)  # По умолчанию с начала
            connection_id = request.data.get('connectionId')  # ID подключения к БД
            
            if not query:
                return JsonResponse({
                    'error': 'Пустой запрос'
                }, status=400)
            
            # Безопасность: проверяем, что запрос не содержит опасные команды
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
            upper_query = query.upper()
            for keyword in dangerous_keywords:
                if keyword in upper_query:
                    return JsonResponse({
                        'error': f'Запросы с командой {keyword} запрещены для безопасности'
                    }, status=400)
            
            # Проверяем, что это SELECT запрос для пагинации
            is_select_query = upper_query.strip().startswith('SELECT')
            
            # Определяем, какое подключение использовать
            if connection_id:
                try:
                    db_connection = DbConnection.objects.get(id=connection_id, is_active=True)
                    if db_connection.database_type == 'iris':
                        cursor = self.get_iris_jdbc_cursor(db_connection)
                    elif db_connection.database_type == 'postgresql':
                        cursor = self.get_postgresql_jdbc_cursor(db_connection)
                    elif db_connection.database_type == 'oracle':
                        cursor = self.get_oracle_jdbc_cursor(db_connection)
                    else:
                        # Для других типов БД используем стандартное подключение Django
                        cursor = connection.cursor()
                except DbConnection.DoesNotExist:
                    return JsonResponse({
                        'error': 'Подключение к БД не найдено или неактивно'
                    }, status=500)
                except Exception as e:
                    return JsonResponse({
                        'error': f'Ошибка подключения к внешней БД: {str(e)}'
                    }, status=500)
            else:
                # Используем стандартное подключение Django
                cursor = connection.cursor()
            
            # Выполняем запрос для подсчета общего количества (только для SELECT)
            total_count = 0
            if is_select_query:
                try:
                    # Создаем запрос для подсчета общего количества записей
                    # Убираем лишние точки с запятой и исправляем синтаксис
                    clean_query = query.rstrip(';')
                    count_query = f"SELECT COUNT(*) FROM ({clean_query}) as subquery"
                    
                    if connection_id:
                        # Для внешних подключений используем соответствующий курсор
                        try:
                            db_connection = DbConnection.objects.get(id=connection_id, is_active=True)
                            if db_connection.database_type == 'iris':
                                # Для IRIS отключаем пагинацию, так как она не работает с этой СУБД
                                total_count = 0
                                limit = None
                                offset = 0
                            elif db_connection.database_type == 'postgresql':
                                count_cursor = self.get_postgresql_jdbc_cursor(db_connection)
                                try:
                                    result_data = self.execute_query_with_jdbc(count_cursor, count_query)
                                    rows = result_data.get('rows', [])
                                    total_count = rows[0][0] if rows else 0
                                finally:
                                    self.close_cursor(count_cursor)
                            elif db_connection.database_type == 'oracle':
                                count_cursor = self.get_oracle_jdbc_cursor(db_connection)
                                try:
                                    result_data = self.execute_query_with_jdbc(count_cursor, count_query)
                                    rows = result_data.get('rows', [])
                                    total_count = rows[0][0] if rows else 0
                                finally:
                                    self.close_cursor(count_cursor)
                            else:
                                # Для других типов БД используем стандартный курсор
                                count_cursor = connection.cursor()
                                count_cursor.execute(count_query)
                                total_count = count_cursor.fetchone()[0]
                                count_cursor.close()
                        except Exception as e:
                            print(f"---Warning: Could not get count for pagination: {e}")
                            if db_connection.database_type == 'iris':
                                # Для IRIS устанавливаем total_count в 0 и отключаем пагинацию
                                total_count = 0
                                limit = None
                                offset = 0
                            else:
                                total_count = 0
                                limit = None
                                offset = 0
                    else:
                        # Для стандартного подключения Django
                        count_cursor = connection.cursor()
                        count_cursor.execute(count_query)
                        total_count = count_cursor.fetchone()[0]
                        count_cursor.close()
                        
                except Exception:
                    # Если не удалось подсчитать, продолжаем без пагинации
                    total_count = 0
                    limit = None
                    offset = 0
            
            # Добавляем LIMIT и OFFSET для пагинации (только для SELECT)
            if is_select_query and limit is not None:
                try:
                    limit = int(limit)
                    offset = int(offset)
                    if limit > 0 and offset >= 0:
                        # Проверяем, нет ли уже LIMIT/OFFSET в запросе
                        if 'LIMIT' not in upper_query and 'OFFSET' not in upper_query:
                            query = f"{query.rstrip(';')} LIMIT {limit} OFFSET {offset}"
                except (ValueError, TypeError):
                    # Некорректные параметры пагинации, игнорируем
                    limit = None
                    offset = 0
            
            # Выполняем основной запрос
            try:
                if connection_id:
                    # Для внешних подключений используем соответствующий курсор
                    if hasattr(cursor, '_connection'):
                        # JDBC курсор для IRIS
                        result_data = self.execute_query_with_jdbc(cursor, query)
                        
                        # Закрываем курсор после использования
                        self.close_cursor(cursor)
                        
                        response_data = {
                            'rows': result_data.get('rows', []),
                            'pagination': {}
                        }
                        
                        # Добавляем информацию о колонках если есть данные
                        if 'columns' in result_data:
                            response_data['columns'] = result_data['columns']
                        elif result_data.get('rows'):
                            # Если колонки не определены, но есть данные
                            response_data['columns'] = [f'Column_{i+1}' for i in range(len(result_data['rows'][0]))]
                        
                        # Добавляем информацию о пагинации для SELECT запросов
                        if is_select_query:
                            response_data['pagination'] = {
                                'total_count': total_count,
                                'limit': limit if limit else len(result_data.get('rows', [])),
                                'offset': offset,
                                'has_next': total_count > offset + len(result_data.get('rows', [])) if total_count > 0 else False,
                                'has_previous': offset > 0,
                                'current_page': (offset // (limit if limit else 50)) + 1 if limit else 1,
                                'total_pages': (total_count + (limit if limit else 50) - 1) // (limit if limit else 50) if total_count > 0 else 1
                            }
                        
                        return JsonResponse(response_data)
                    else:
                        # Стандартный курсор Django
                        cursor.execute(query)
                        # Дальше стандартная обработка...
                        if cursor.description:
                            columns = [col[0] for col in cursor.description]
                            rows = cursor.fetchall()
                            
                            # Преобразуем строки в списки для JSON сериализации
                            data = []
                            for row in rows:
                                data.append(list(row))
                            
                            response_data = {
                                'columns': columns,
                                'rows': data,
                                'pagination': {}
                            }
                            
                            # Добавляем информацию о пагинации для SELECT запросов
                            if is_select_query:
                                response_data['pagination'] = {
                                    'total_count': total_count,
                                    'limit': limit if limit else len(data),
                                    'offset': offset,
                                    'has_next': total_count > offset + len(data) if total_count > 0 else False,
                                    'has_previous': offset > 0,
                                    'current_page': (offset // (limit if limit else 50)) + 1 if limit else 1,
                                    'total_pages': (total_count + (limit if limit else 50) - 1) // (limit if limit else 50) if total_count > 0 else 1
                                }
                            
                            return JsonResponse(response_data)
                        else:
                            # Для команд, которые не возвращают данные
                            affected_rows = cursor.rowcount
                            return JsonResponse({
                                'message': 'Запрос выполнен успешно',
                                'affected_rows': affected_rows
                            })
                else:
                    # Стандартная обработка для Django подключения
                    cursor.execute(query)
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                        rows = cursor.fetchall()
                        
                        # Преобразуем строки в списки для JSON сериализации
                        data = []
                        for row in rows:
                            data.append(list(row))
                        
                        response_data = {
                            'columns': columns,
                            'rows': data,
                            'pagination': {}
                        }
                        
                        # Добавляем информацию о пагинации для SELECT запросов
                        if is_select_query:
                            response_data['pagination'] = {
                                'total_count': total_count,
                                'limit': limit if limit else len(data),
                                'offset': offset,
                                'has_next': total_count > offset + len(data) if total_count > 0 else False,
                                'has_previous': offset > 0,
                                'current_page': (offset // (limit if limit else 50)) + 1 if limit else 1,
                                'total_pages': (total_count + (limit if limit else 50) - 1) // (limit if limit else 50) if total_count > 0 else 1
                            }
                        
                        return JsonResponse(response_data)
                    else:
                        # Для команд, которые не возвращают данные
                        affected_rows = cursor.rowcount
                        return JsonResponse({
                            'message': 'Запрос выполнен успешно',
                            'affected_rows': affected_rows
                        })
                        
            finally:
                # Всегда закрываем курсор если это JDBC курсор
                if connection_id and hasattr(cursor, '_connection'):
                    self.close_cursor(cursor)
                elif not connection_id:
                    # Для стандартного курсора Django
                    try:
                        cursor.close()
                    except:
                        pass
                        
        except Exception as e:
            # Обеспечиваем закрытие курсора в случае ошибки
            if connection_id and hasattr(cursor, '_connection'):
                self.close_cursor(cursor)
            return JsonResponse({
                'error': f'Ошибка выполнения запроса: {str(e)}'
            }, status=500)
    
    @extend_schema(
        description='Тестирование подключения к базе данных',
        summary='Тест подключения'
    )
    def test_connection(self, request):
        """Тестирование подключения к БД"""
        try:
            connection_data = request.data.get('connection', {})
            
            if not connection_data:
                return JsonResponse({
                    'error': 'Данные подключения не предоставлены'
                }, status=400)
            
            # Валидация данных подключения
            # Поддерживаем как camelCase (от frontend), так и snake_case (backwards compatibility)
            connection_string = (
                connection_data.get('connectionString') or
                connection_data.get('connection_string')
            )
            username = connection_data.get('username')
            password = connection_data.get('password', '')
            database_type = (
                connection_data.get('databaseType') or
                connection_data.get('database_type', 'postgresql')
            )
            
            required_fields = ['connectionString', 'connection_string', 'username']
            if not any(connection_data.get(field) for field in ['connectionString', 'connection_string']) or not username:
                return JsonResponse({
                    'error': 'Поля connectionString/connection_string и username обязательны'
                }, status=400)
            
            if database_type == 'iris':
                return self.test_iris_connection(connection_string, username, password)
            else:
                return self.test_standard_db_connection(connection_string, username, password, database_type)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка тестирования подключения: {str(e)}'
            }, status=500)
    
    def test_iris_connection(self, connection_string, username, password):
        """Тестирование подключения к IRIS через JDBC"""
        try:
            # Более гибкая валидация строки подключения IRIS
            if not connection_string:
                return JsonResponse({
                    'success': False,
                    'error': 'Строка подключения не может быть пустой'
                }, status=400)
            
            # Проверяем, что это IRIS JDBC URL (разрешаем различные варианты)
            connection_upper = connection_string.upper()
            if not (connection_upper.startswith('JDBC:IRIS://') or connection_upper.startswith('JDBC:CACHE://')):
                return JsonResponse({
                    'success': False,
                    'error': f'Строка подключения должна начинаться с jdbc:IRIS:// или jdbc:cache://. Получено: {connection_string}'
                }, status=400)
            
            # Парсим JDBC URL для извлечения информации
            try:
                o = urlparse(connection_string)
                if not o.hostname:
                    # Пытаемся извлечь хост и порт вручную если urlparse не сработал
                    # Формат: jdbc:IRIS://host:port/NAMESPACE
                    if '://' in connection_string:
                        after_protocol = connection_string.split('://', 1)[1]
                        if '/' in after_protocol:
                            host_port_part = after_protocol.split('/')[0]
                            if ':' in host_port_part:
                                host_part, port_part = host_port_part.rsplit(':', 1)
                                hostname = host_part
                                try:
                                    port = int(port_part)
                                except ValueError:
                                    port = 1972  # Порт по умолчанию для IRIS
                            else:
                                hostname = host_port_part
                                port = 1972  # Порт по умолчанию для IRIS
                        else:
                            hostname = 'localhost'
                            port = 1972
                    else:
                        hostname = 'localhost'
                        port = 1972
                else:
                    hostname = o.hostname
                    port = o.port or 1972
            except Exception as e:
                print(f"---Warning: Could not parse connection string: {e}")
                hostname = 'localhost'
                port = 1972
            
            # Определяем JAR файлы для IRIS JDBC драйверов
            iris_jars = IRIS_JARS
            
            print(f"---Testing IRIS JDBC connection to {hostname}:{port}")
            print(f"---Using JAR: {iris_jars}")
            print(f"---Connection string: {connection_string}")
            print(f"---Username: {username}")
            
            # Пробуем разные имена драйверов IRIS
            iris_drivers = [
                'com.intersystems.jdbc.IRISDriver',
            ]
            
            con = None
            last_error = None
            
            for driver_class in iris_drivers:
                try:
                    print(f"---Trying driver: {driver_class}")
                    con = jaydebeapi.connect(
                        driver_class,
                        connection_string,
                        [username, password],
                        jars=[iris_jars]
                    )
                    print(f"---Successfully connected with driver: {driver_class}")
                    break
                except Exception as e:
                    print(f"---Failed with driver {driver_class}: {e}")
                    last_error = e
                    con = None
                    continue
            
            if con is None:
                raise Exception(f"Не удалось подключиться ни с одним из драйверов IRIS. Последняя ошибка: {last_error}")
            
            print(f"---IRIS connection established successfully")
            
            # Тестовый запрос
            curs = con.cursor()
            test_query = "SELECT 1 as test_result"
            curs.execute(test_query)
            result = curs.fetchone()
            
            if result and result[0] == 1:
                con.close()
                
                # Извлекаем namespace из строки подключения
                namespace = 'USER'  # По умолчанию
                try:
                    if '/' in o.path:
                        namespace = o.path.split('/')[1] if o.path else 'USER'
                except:
                    namespace = 'USER'
                
                return JsonResponse({
                    'success': True,
                    'message': f'Подключение к IRIS успешно установлено',
                    'connection_info': {
                        'type': 'iris',
                        'host': hostname,
                        'port': port,
                        'namespace': namespace,
                        'status': 'connected',
                        'jdbc_url': connection_string,
                        'driver': 'com.intersystems.jdbc.IRISDriver'
                    }
                })
            else:
                con.close()
                return JsonResponse({
                    'success': False,
                    'error': 'Неожиданный результат тестового запроса. Получен: ' + str(result)
                }, status=500)
                
        except Exception as err:
            print(f"---IRIS JDBC test error: {err}")
            
            # Более информативные сообщения об ошибках
            error_message = str(err)
            if 'Connection refused' in error_message:
                return JsonResponse({
                    'success': False,
                    'error': 'Подключение отклонено. Проверьте, что IRIS сервер запущен и доступен по указанному адресу'
                }, status=500)
            elif 'Authentication failed' in error_message or 'Login failed' in error_message:
                return JsonResponse({
                    'success': False,
                    'error': 'Неверные учетные данные (имя пользователя или пароль)'
                }, status=500)
            elif 'Network' in error_message or 'timeout' in error_message.lower():
                return JsonResponse({
                    'success': False,
                    'error': 'Ошибка сети. Проверьте сетевое подключение и доступность сервера'
                }, status=500)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Ошибка подключения к IRIS: {error_message}'
                }, status=500)
    
    def test_standard_db_connection(self, connection_string, username, password, database_type):
        """Тестирование стандартных подключений к БД (PostgreSQL, Oracle)"""
        try:
            # Гибкая валидация строки подключения - поддерживаем и обычные URL, и JDBC
            if not connection_string.startswith(('jdbc:', database_type + '://')):
                return JsonResponse({
                    'success': False,
                    'error': f'Строка подключения должна начинаться с {database_type}:// или jdbc:{database_type}://'
                }, status=400)
            
            # Если строка не начинается с jdbc:, добавляем префикс
            if not connection_string.startswith('jdbc:'):
                if database_type == 'postgresql':
                    connection_string = 'jdbc:' + connection_string
                elif database_type == 'oracle':
                    # Oracle требует специальной обработки
                    connection_string = 'jdbc:oracle:thin:' + connection_string
                else:
                    connection_string = 'jdbc:' + connection_string
            
            # Определяем JDBC драйвер и параметры подключения
            if database_type == 'postgresql':
                return self.test_postgresql_connection(connection_string, username, password)
            elif database_type == 'oracle':
                return self.test_oracle_connection(connection_string, username, password)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Неподдерживаемый тип базы данных: {database_type}'
                }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка тестирования подключения к {database_type}: {str(e)}'
            }, status=500)
    
    def test_postgresql_connection(self, connection_string, username, password):
        """Тестирование подключения к PostgreSQL через psycopg2"""
        try:
            # Импортируем psycopg2 для подключения к PostgreSQL
            import psycopg2
            from urllib.parse import urlparse
            
            print(f"---Testing PostgreSQL psycopg2 connection")
            print(f"---Connection string: {connection_string}")
            print(f"---Username: {username}")
            
            # Парсим JDBC строку подключения для извлечения информации
            # Формат JDBC: jdbc:postgresql://host:port/database
            jdbc_url = connection_string
            if jdbc_url.startswith('jdbc:postgresql://'):
                # Убираем префикс jdbc:postgresql://
                url_part = jdbc_url[len('jdbc:postgresql://'):]
                
                # Разбираем строку подключения
                parsed_url = urlparse(f'postgresql://{url_part}')
                
                # Извлекаем компоненты
                host = parsed_url.hostname
                port = parsed_url.port or 5432
                database = parsed_url.path.lstrip('/')
                
                # Используем параметры из функции
                username = username
                password = password
                
                # Создаем подключение через psycopg2
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    password=password
                )
                
                # Тестовый запрос
                curs = conn.cursor()
                test_query = "SELECT 1 as test_result"
                curs.execute(test_query)
                result = curs.fetchone()
                
                if result and result[0] == 1:
                    conn.close()
                    return JsonResponse({
                        'success': True,
                        'message': f'Подключение к PostgreSQL успешно',
                        'connection_info': {
                            'type': 'postgresql',
                            'host': host,
                            'port': port,
                            'database': database,
                            'status': 'connected',
                            'jdbc_url': connection_string
                        }
                    })
                else:
                    conn.close()
                    return JsonResponse({
                        'success': False,
                        'error': 'Неожиданный результат тестового запроса'
                    }, status=500)
            else:
                raise Exception(f'Неподдерживаемый формат строки подключения: {jdbc_url}')
                
        except Exception as err:
            print(f"---PostgreSQL psycopg2 test error: {err}")
            return JsonResponse({
                'success': False,
                'error': f'Ошибка подключения к PostgreSQL: {str(err)}'
            }, status=500)
    
    def test_oracle_connection(self, connection_string, username, password):
        """Тестирование подключения к Oracle через JDBC"""
        try:
            # Парсим строку подключения для извлечения информации
            # Oracle JDBC URL имеет формат: jdbc:oracle:thin:@host:port:service_name
            # или jdbc:oracle:thin:@//host:port/service_name
            
            host = 'localhost'
            port = 1521
            database = 'XE'  # По умолчанию
            
            # Извлекаем информацию из строки подключения Oracle
            if '@' in connection_string:
                after_at = connection_string.split('@')[1]
                if ':' in after_at:
                    if '//' in after_at:
                        # Формат: jdbc:oracle:thin:@//host:port/service_name
                        url_part = after_at.replace('//', '')
                        parts = url_part.split('/')
                        if len(parts) >= 2:
                            host_port = parts[0].split(':')
                            host = host_port[0] if host_port[0] else 'localhost'
                            port = int(host_port[1]) if len(host_port) > 1 else 1521
                            database = parts[1] if len(parts) > 1 else 'XE'
                    else:
                        # Формат: jdbc:oracle:thin:@host:port:service_name
                        host_port_db = after_at.split(':')
                        if len(host_port_db) >= 3:
                            host = host_port_db[0] if host_port_db[0] else 'localhost'
                            port = int(host_port_db[1]) if host_port_db[1] else 1521
                            database = host_port_db[2] if host_port_db[2] else 'XE'
            
            # Определяем JAR файлы для Oracle JDBC драйвера
            oracle_jars = [
                'appmsw/java/ojdbc6.jar'
            ]
            
            print(f"---Testing Oracle JDBC connection to {host}:{port}/{database}")
            
            # Создаем подключение через JDBC
            con = jaydebeapi.connect(
                'oracle.jdbc.driver.OracleDriver',
                connection_string,
                [username, password],
                jars=[oracle_jars]
            )
            
            # Тестовый запрос
            curs = con.cursor()
            test_query = "SELECT 1 as test_result FROM dual"
            curs.execute(test_query)
            result = curs.fetchone()
            
            if result and result[0] == 1:
                con.close()
                return JsonResponse({
                    'success': True,
                    'message': f'Подключение к Oracle успешно',
                    'connection_info': {
                        'type': 'oracle',
                        'host': host,
                        'port': port,
                        'database': database,
                        'status': 'connected',
                        'jdbc_url': connection_string
                    }
                })
            else:
                con.close()
                return JsonResponse({
                    'success': False,
                    'error': 'Неожиданный результат тестового запроса'
                }, status=500)
                
        except Exception as err:
            print(f"---Oracle JDBC test error: {err}")
            return JsonResponse({
                'success': False,
                'error': f'Ошибка подключения к Oracle: {str(err)}'
            }, status=500)
    
    @extend_schema(
        description='Получить список сохраненных подключений к БД',
        summary='Список подключений'
    )
    def list_connections(self, request):
        """Получить список сохраненных подключений к БД"""
        try:
            connections = DbConnection.objects.filter(
                models.Q(user=request.user) | models.Q(is_active=True)
            )
            
            connections_data = []
            for conn in connections:
                connections_data.append({
                    'id': conn.id,
                    'name': conn.name,
                    'database_type': conn.database_type,
                    'connection_string': conn.connection_string,
                    'username': conn.username,
                    'password': conn.password,  # Добавляем поле password
                    'description': conn.description,
                    'is_active': conn.is_active,
                    'created_date': conn.created_date,
                    'updated_date': conn.updated_date
                })
            
            return JsonResponse({
                'connections': connections_data
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка получения списка подключений: {str(e)}'
            }, status=500)
    
    @extend_schema(
        description='Создать новое подключение к БД',
        summary='Создание подключения'
    )
    def create_connection(self, request):
        """Создать новое подключение к БД"""
        try:
            connection_data = request.data.get('connection', {})
            
            if not connection_data:
                return JsonResponse({
                    'error': 'Данные подключения не предоставлены'
                }, status=400)
            
            # Создаем новое подключение
            connection = DbConnection.objects.create(
                name=connection_data.get('name'),
                database_type=connection_data.get('database_type'),
                connection_string=connection_data.get('connection_string'),
                username=connection_data.get('username'),
                password=connection_data.get('password', ''),
                description=connection_data.get('description', ''),
                is_active=True,
                user=request.user
            )
            
            return JsonResponse({
                'success': True,
                'connection': {
                    'id': connection.id,
                    'name': connection.name,
                    'database_type': connection.database_type,
                    'connection_string': connection.connection_string,
                    'username': connection.username,
                    'password': connection.password,  # Добавляем поле password
                    'description': connection.description,
                    'is_active': connection.is_active
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка создания подключения: {str(e)}'
            }, status=500)
    
    def get_connection(self, request, connection_id):
        """Получить детали подключения к БД"""
        try:
            connection = DbConnection.objects.filter(
                id=connection_id
            ).filter(
                models.Q(user=request.user) | models.Q(is_active=True)
            ).first()
            
            if not connection:
                raise DbConnection.DoesNotExist()
            
            connection_data = {
                'id': connection.id,
                'name': connection.name,
                'database_type': connection.database_type,
                'connection_string': connection.connection_string,
                'username': connection.username,
                'password': connection.password,  # Добавляем поле password
                'description': connection.description,
                'is_active': connection.is_active,
                'created_date': connection.created_date,
                'updated_date': connection.updated_date
            }
            
            return JsonResponse({
                'connection': connection_data
            })
            
        except DbConnection.DoesNotExist:
            return JsonResponse({
                'error': 'Подключение не найдено'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка получения подключения: {str(e)}'
            }, status=500)
    
    def update_connection(self, request, connection_id):
        """Обновить подключение к БД"""
        try:
            connection = DbConnection.objects.get(
                id=connection_id,
                user=request.user
            )
            
            connection_data = request.data.get('connection', {})
            
            # Обновляем поля подключения
            for field in ['name', 'database_type', 'connection_string', 'username', 'password', 'description', 'is_active']:
                if field in connection_data:
                    setattr(connection, field, connection_data[field])
            
            connection.save()
            
            return JsonResponse({
                'success': True,
                'connection': {
                    'id': connection.id,
                    'name': connection.name,
                    'database_type': connection.database_type,
                    'connection_string': connection.connection_string,
                    'username': connection.username,
                    'password': connection.password,  # Добавляем поле password
                    'description': connection.description,
                    'is_active': connection.is_active
                }
            })
            
        except DbConnection.DoesNotExist:
            return JsonResponse({
                'error': 'Подключение не найдено или недоступно для редактирования'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка обновления подключения: {str(e)}'
            }, status=500)
    
    def delete_connection(self, request, connection_id):
        """Удалить подключение к БД"""
        try:
            connection = DbConnection.objects.get(
                id=connection_id,
                user=request.user
            )
            
            connection.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Подключение успешно удалено'
            })
            
        except DbConnection.DoesNotExist:
            return JsonResponse({
                'error': 'Подключение не найдено или недоступно для удаления'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка удаления подключения: {str(e)}'
            }, status=500)
    
    def get_iris_jdbc_cursor(self, db_connection):
        """Создать курсор для IRIS JDBC подключения"""
        try:
            # Определяем JAR файлы для IRIS JDBC драйверов
            iris_jars = IRIS_JARS
            
            print(f"---Using IRIS JDBC JAR: {iris_jars}")
            print(f"---Connection string: {db_connection.connection_string}")
            print(f"---Username: {db_connection.username}")
            
            # Пробуем разные имена драйверов IRIS
            iris_drivers = [
                'com.intersystems.jdbc.IRISDriver',
               ]
            
            con = None
            last_error = None
            
            for driver_class in iris_drivers:
                try:
                    print(f"---Trying driver: {driver_class}")
                    # Проверяем, является ли iris_jars строкой или списком
                    if isinstance(iris_jars, str):
                        jars_to_use = iris_jars
                    else:
                        jars_to_use = iris_jars[0] if iris_jars else ''
                    
                    con = jaydebeapi.connect(
                        driver_class,
                        db_connection.connection_string,
                        [db_connection.username, db_connection.password],
                        jars=jars_to_use
                    )
                    print(f"---Successfully connected with driver: {driver_class}")
                    break
                except Exception as e:
                    print(f"---Failed with driver {driver_class}: {e}")
                    last_error = e
                    con = None
                    continue
            
            if con is None:
                raise Exception(f'Ошибка подключения к IRIS: Не удалось подключиться ни с одним из драйверов. Последняя ошибка: {last_error}')
            
            # Создаем курсор
            cursor = con.cursor()
            
            # Сохраняем соединение для последующего закрытия
            cursor._connection = con
            
            return cursor
            
        except Exception as err:
            print(f"---IRIS JDBC connection error: {err}")
            raise Exception(f'Ошибка подключения к IRIS: {str(err)}')
    
    def get_postgresql_jdbc_cursor(self, db_connection):
        """Создать курсор для PostgreSQL JDBC подключения"""
        try:
            # Импортируем psycopg2 для подключения к PostgreSQL
            import psycopg2
            from urllib.parse import urlparse
            
            print(f"---Connection string: {db_connection.connection_string}")
            print(f"---Username: {db_connection.username}")
            
            # Парсим JDBC строку подключения для извлечения информации
            # Формат JDBC: jdbc:postgresql://host:port/database
            jdbc_url = db_connection.connection_string
            if jdbc_url.startswith('jdbc:postgresql://'):
                # Убираем префикс jdbc:postgresql://
                url_part = jdbc_url[len('jdbc:postgresql://'):]
                
                # Разбираем строку подключения
                parsed_url = urlparse(f'postgresql://{url_part}')
                
                # Извлекаем компоненты
                host = parsed_url.hostname
                port = parsed_url.port or 5432
                database = parsed_url.path.lstrip('/')
                
                # Используем параметры из db_connection
                username = db_connection.username
                password = db_connection.password
                
                # Создаем подключение через psycopg2
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    password=password
                )
                
                # Создаем курсор
                cursor = conn.cursor()
                
                # Создаем объект-обертку для курсора, чтобы добавить к нему атрибут connection
                class CursorWrapper:
                    def __init__(self, cursor, connection):
                        self.cursor = cursor
                        self.connection = connection
                    
                    def __getattr__(self, name):
                        # Делегируем все неопределенные атрибуты внутреннему курсору
                        return getattr(self.cursor, name)
                
                wrapped_cursor = CursorWrapper(cursor, conn)
                
                print(f"---PostgreSQL psycopg2 connection successful")
                return wrapped_cursor
            else:
                raise Exception(f'Неподдерживаемый формат строки подключения: {jdbc_url}')
                
        except Exception as err:
            print(f"---PostgreSQL psycopg2 connection error: {err}")
            import traceback
            traceback.print_exc()
            raise Exception(f'Ошибка подключения к PostgreSQL: {str(err)}')
    
    def get_oracle_jdbc_cursor(self, db_connection):
        """Создать курсор для Oracle JDBC подключения"""
        try:
            # Определяем JAR файл для Oracle JDBC драйвера
            import os
            from django.conf import settings
            BASE_DIR = settings.BASE_DIR
            oracle_jars = os.path.join(BASE_DIR, 'appmsw', 'java', 'ojdbc6.jar')
            
            print(f"---Using Oracle JDBC JAR: {oracle_jars}")
            print(f"---Connection string: {db_connection.connection_string}")
            print(f"---Username: {db_connection.username}") #print(f"---Username: {db_connection.username} pass:{db_connection.password}")
            
            # Проверяем существование JAR файла
            if not os.path.exists(oracle_jars):
                raise Exception(f"JAR файл не найден: {oracle_jars}")
            
            # Подключаемся к Oracle через JDBC
            con = jaydebeapi.connect(
                'oracle.jdbc.driver.OracleDriver',
                db_connection.connection_string,
                [db_connection.username, db_connection.password],
                jars=oracle_jars
            )
            
            # Создаем курсор
            cursor = con.cursor()
            
            # Сохраняем соединение для последующего закрытия
            cursor._connection = con
            
            return cursor
            
        except Exception as err:
            print(f"---Oracle JDBC connection error: {err}")
            raise Exception(f'Ошибка подключения к Oracle: {str(err)}')
    
    def close_cursor(self, cursor):
        """Безопасное закрытие курсора и соединения"""
        try:
            if hasattr(cursor, 'connection'):
                cursor.connection.close()
            elif hasattr(cursor, 'close'):
                cursor.close()
        except Exception as e:
            print(f"---Error closing cursor: {e}")
    
    def execute_query_with_jdbc(self, cursor, query):
        """Выполнить запрос через JDBC курсор"""
        try:
            print(f"---Executing JDBC query: {query[:100]}...")
            
            # Выполняем запрос
            cursor.execute(query)
            
            # Получаем метаданные столбцов
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Преобразуем строки в списки для JSON сериализации
                data = []
                for row in rows:
                    data.append(list(row))
                
                return {
                    'columns': columns,
                    'rows': data
                }
            else:
                # Для команд, которые не возвращают данные
                affected_rows = cursor.rowcount
                return {
                    'affected_rows': affected_rows
                }
                
        except Exception as e:
            error_msg = str(e)
            # Проверяем, связана ли ошибка с INTO clause
            if "INTO clause" in error_msg or "INTO" in error_msg:
                # Для IRIS баз данных могут быть специфические ограничения
                # Попробуем обработать запрос особым образом
                raise Exception(f'Ошибка выполнения JDBC запроса (возможно, проблема с синтаксисом для IRIS): {error_msg}')
            else:
                raise Exception(f'Ошибка выполнения JDBC запроса: {error_msg}')

class ChatRAGAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        description='Получить список доступных моделей из Ollama',
        summary='Список моделей'
    )
    def get(self, request):
        """Получить список доступных моделей из Ollama"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Получаем URL Ollama из системных параметров
            ollama_url = self.get_ollama_url()
            logger.info(f"ChatRAG GET: Получен Ollama URL: {ollama_url}")
            
            if not ollama_url:
                logger.error("ChatRAG GET: URL Ollama сервера не настроен")
                return JsonResponse({
                    'error': 'URL Ollama сервера не настроен в системных параметрах'
                }, status=400)
            
            # Получаем список моделей с Ollama сервера
            import requests
            
            # Настраиваем прокси (обход для локальных адресов)
            proxies = self.get_proxies(ollama_url)
            logger.info(f"ChatRAG GET: Используемые прокси: {proxies}")
            
            logger.info(f"ChatRAG GET: Отправка запроса к {ollama_url}/api/tags")
            response = requests.get(f'{ollama_url}/api/tags', timeout=10, proxies=proxies)
            response.raise_for_status()
            logger.info(f"ChatRAG GET: Успешный ответ, статус код: {response.status_code}")
            
            models_data = response.json()
            models = []
            
            if 'models' in models_data:
                for model in models_data['models']:
                    models.append({
                        'name': model.get('name', ''),
                        'size': model.get('size', 0),
                        'modified_at': model.get('modified_at', '')
                    })
            
            return JsonResponse({
                'models': models,
                'ollama_url': ollama_url
            })
            
        except requests.exceptions.RequestException as e:
            logger.error(f"ChatRAG GET: Ошибка подключения к Ollama: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка подключения к Ollama серверу: {str(e)}'
            }, status=503)
        except Exception as e:
            logger.error(f"ChatRAG GET: Общая ошибка: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка получения списка моделей: {str(e)}'
            }, status=500)
    
    def post(self, request):
        """Обработка запроса к RAG модели"""
        # Проверяем, это ли это ollama-url endpoint
        if request.path.endswith('/ollama-url/'):
            return self.handle_ollama_url_request(request)
        
        import logging
        import json as json_module
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 80)
        logger.info("ChatRAG POST: НАЧАЛО ОБРАБОТКИ ЗАПРОСА")
        logger.info("=" * 80)
        
        try:
            # Логируем входящие данные запроса
            logger.info(f"ChatRAG POST: Входящие данные запроса (request.data):")
            logger.info(f"  - Тип данных: {type(request.data)}")
            try:
                logger.info(f"  - Содержимое: {json_module.dumps(dict(request.data), ensure_ascii=False, indent=2, default=str)}")
            except Exception as e:
                logger.info(f"  - Содержимое (raw): {request.data}")
            
            question = request.data.get('question', '').strip()
            model = request.data.get('model', 'llama2').strip()
            chat_history = request.data.get('chat_history', [])
            
            # Получаем параметры модели из запроса
            temperature = request.data.get('temperature', 0.7)
            top_p = request.data.get('top_p', 0.9)
            max_tokens = request.data.get('max_tokens', 1000)
            use_system_context = request.data.get('use_system_context', True)
            custom_system_prompt = request.data.get('system_prompt', None)
            
            logger.info(f"ChatRAG POST: Извлеченные параметры:")
            logger.info(f"  - Вопрос: '{question[:100]}...' (длина: {len(question)})")
            logger.info(f"  - Модель: {model}")
            logger.info(f"  - История чата: {len(chat_history)} сообщений")
            logger.info(f"  - temperature: {temperature} (тип: {type(temperature)})")
            logger.info(f"  - top_p: {top_p} (тип: {type(top_p)})")
            logger.info(f"  - max_tokens: {max_tokens} (тип: {type(max_tokens)})")
            logger.info(f"  - use_system_context: {use_system_context}")
            logger.info(f"  - custom_system_prompt: {'Да (длина: ' + str(len(custom_system_prompt)) + ')' if custom_system_prompt else 'Нет'}")
            
            if not question:
                logger.warning("ChatRAG POST: Пустой вопрос")
                return JsonResponse({
                    'error': 'Вопрос не может быть пустым'
                }, status=400)
            
            # Получаем URL Ollama из системных параметров
            ollama_url = self.get_ollama_url()
            logger.info(f"ChatRAG POST: Получен Ollama URL: {ollama_url}")
            
            if not ollama_url:
                logger.error("ChatRAG POST: URL Ollama сервера не настроен")
                return JsonResponse({
                    'error': 'URL Ollama сервера не настроен в системных параметрах'
                }, status=400)
            
            # Подготавливаем контекст из истории чата
            logger.info("-" * 40)
            logger.info("ChatRAG POST: ФОРМИРОВАНИЕ КОНТЕКСТА")
            logger.info("-" * 40)
            
            context = ""
            if chat_history and len(chat_history) > 0:
                context_parts = []
                for i, msg in enumerate(chat_history):
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')
                    logger.info(f"  История [{i}]: role={role}, content_length={len(content)}")
                    if role == 'user':
                        context_parts.append(f"Пользователь: {content}")
                    elif role == 'assistant':
                        context_parts.append(f"Ассистент: {content}")
                context = "\n".join(context_parts)
                logger.info(f"ChatRAG POST: Сформирован контекст из {len(chat_history)} сообщений (длина: {len(context)})")
            else:
                logger.info("ChatRAG POST: История чата пуста")
            
            # Добавляем контекст о системных данных (если включено)
            system_context = ""
            if use_system_context:
                system_context = self.get_system_context()
                logger.info(f"ChatRAG POST: Добавлен системный контекст (длина: {len(system_context)})")
                logger.info(f"ChatRAG POST: Системный контекст:\n{system_context}")
            else:
                logger.info("ChatRAG POST: Системный контекст отключен")
            
            # Формируем полный промпт
            logger.info("-" * 40)
            logger.info("ChatRAG POST: ФОРМИРОВАНИЕ ПРОМПТА")
            logger.info("-" * 40)
            
            if custom_system_prompt:
                # Используем пользовательский системный промпт
                logger.info(f"ChatRAG POST: Используется ПОЛЬЗОВАТЕЛЬСКИЙ системный промпт:")
                logger.info(f"  {custom_system_prompt[:200]}...")
                full_prompt = f"""{custom_system_prompt}

Системная информация:
{system_context}

Предыдущая беседа:
{context}

Текущий вопрос пользователя: {question}"""
            else:
                # Используем промпт по умолчанию
                logger.info("ChatRAG POST: Используется СТАНДАРТНЫЙ системный промпт")
                full_prompt = f"""Ты - RAG ассистент для работы с системой управления параметрами.

Системная информация:
{system_context}

Предыдущая беседа:
{context}

Текущий вопрос пользователя: {question}
"""
# Отвечай на русском языке, используя доступную информацию из системных данных. Если информации недостаточно, четко об этом скажи.
            
            logger.info(f"ChatRAG POST: Полный промпт (длина: {len(full_prompt)}):")
            logger.info("=" * 80)
            logger.info("НАЧАЛО ПРОМПТА")
            logger.info("=" * 80)
            logger.info(full_prompt)
            logger.info("=" * 80)
            logger.info("КОНЕЦ ПРОМПТА")
            logger.info("=" * 80)

            # Отправляем запрос к Ollama
            import requests
            
            logger.info("-" * 40)
            logger.info("ChatRAG POST: ВАЛИДАЦИЯ И ПОДГОТОВКА ПАРАМЕТРОВ")
            logger.info("-" * 40)
            
            # Валидация параметров
            try:
                temperature = float(temperature)
                top_p = float(top_p)
                max_tokens = int(max_tokens)
                
                logger.info(f"ChatRAG POST: Параметры после преобразования типов:")
                logger.info(f"  - temperature: {temperature} (float)")
                logger.info(f"  - top_p: {top_p} (float)")
                logger.info(f"  - max_tokens: {max_tokens} (int)")
                
                # Ограничиваем значения
                original_temp = temperature
                original_top_p = top_p
                original_max_tokens = max_tokens
                
                temperature = max(0.0, min(2.0, temperature))
                top_p = max(0.0, min(1.0, top_p))
                max_tokens = max(100, min(4000, max_tokens))
                
                if original_temp != temperature or original_top_p != top_p or original_max_tokens != max_tokens:
                    logger.warning(f"ChatRAG POST: Параметры были ограничены:")
                    logger.warning(f"  - temperature: {original_temp} -> {temperature}")
                    logger.warning(f"  - top_p: {original_top_p} -> {top_p}")
                    logger.warning(f"  - max_tokens: {original_max_tokens} -> {max_tokens}")
                
            except (ValueError, TypeError) as e:
                logger.warning(f"ChatRAG POST: Ошибка валидации параметров: {e}, используются значения по умолчанию")
                temperature = 0.7
                top_p = 0.9
                max_tokens = 1000
            
            payload = {
                'model': model,
                'prompt': full_prompt,
                'stream': False,
                'options': {
                    'temperature': temperature,
                    'top_p': top_p,
                    'max_tokens': max_tokens
                }
            }
            
            logger.info("-" * 40)
            logger.info("ChatRAG POST: ОТПРАВКА ЗАПРОСА К OLLAMA")
            logger.info("-" * 40)
            
            logger.info(f"ChatRAG POST: Payload для Ollama:")
            logger.info(f"  - model: {payload['model']}")
            logger.info(f"  - prompt_length: {len(payload['prompt'])}")
            logger.info(f"  - stream: {payload['stream']}")
            logger.info(f"  - options: {json_module.dumps(payload['options'], indent=2)}")
            logger.info("-" * 80)
            logger.info("ПОЛНЫЙ PAYLOAD PROMPT:")
            logger.info("-" * 80)
            logger.info(payload['prompt'])
            logger.info("-" * 80)
            
            # Настраиваем прокси (обход для локальных адресов)
            proxies = self.get_proxies(ollama_url)
            logger.info(f"ChatRAG POST: Используемые прокси: {proxies}")
            
            request_url = f'{ollama_url}/api/generate'
            logger.info(f"ChatRAG POST: URL запроса: {request_url}")
            logger.info(f"ChatRAG POST: Timeout: 120 секунд")
            
            import time
            start_time = time.time()
            
            response = requests.post(request_url, json=payload, timeout=120, proxies=proxies)
            
            elapsed_time = time.time() - start_time
            logger.info(f"ChatRAG POST: Время выполнения запроса: {elapsed_time:.2f} секунд")
            
            logger.info("-" * 40)
            logger.info("ChatRAG POST: ОТВЕТ ОТ OLLAMA")
            logger.info("-" * 40)
            
            logger.info(f"ChatRAG POST: HTTP статус код: {response.status_code}")
            logger.info(f"ChatRAG POST: HTTP заголовки ответа:")
            for header, value in response.headers.items():
                logger.info(f"  - {header}: {value}")
            
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(f"ChatRAG POST: Полный JSON ответ от Ollama:")
            logger.info(json_module.dumps(result, ensure_ascii=False, indent=2, default=str))
            
            answer = result.get('response', 'Извините, не удалось получить ответ от модели.')
            
            logger.info(f"ChatRAG POST: Извлеченный ответ (длина: {len(answer)}):")
            logger.info(f"  {answer[:500]}..." if len(answer) > 500 else f"  {answer}")
            
            # Дополнительная информация из ответа Ollama
            ollama_stats = {
                'total_duration': result.get('total_duration'),
                'load_duration': result.get('load_duration'),
                'prompt_eval_count': result.get('prompt_eval_count'),
                'prompt_eval_duration': result.get('prompt_eval_duration'),
                'eval_count': result.get('eval_count'),
                'eval_duration': result.get('eval_duration'),
                'context': result.get('context'),
                'done': result.get('done'),
                'done_reason': result.get('done_reason')
            }
            
            logger.info(f"ChatRAG POST: Статистика Ollama:")
            for key, value in ollama_stats.items():
                if value is not None:
                    logger.info(f"  - {key}: {value}")
            
            logger.info("=" * 80)
            logger.info("ChatRAG POST: ЗАВЕРШЕНИЕ ОБРАБОТКИ ЗАПРОСА (УСПЕХ)")
            logger.info("=" * 80)
            
            return JsonResponse({
                'answer': answer,
                'model_used': model,
                'context_length': len(system_context),
                'params_used': {
                    'temperature': temperature,
                    'top_p': top_p,
                    'max_tokens': max_tokens,
                    'use_system_context': use_system_context
                },
                'ollama_stats': ollama_stats,
                'request_time': elapsed_time
            })
            
        except requests.exceptions.RequestException as e:
            logger.error("=" * 80)
            logger.error("ChatRAG POST: ОШИБКА ПОДКЛЮЧЕНИЯ К OLLAMA")
            logger.error("=" * 80)
            logger.error(f"ChatRAG POST: Тип ошибки: {type(e).__name__}")
            logger.error(f"ChatRAG POST: Сообщение: {str(e)}")
            logger.error(f"ChatRAG POST: Полная трассировка:", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка подключения к Ollama серверу: {str(e)}'
            }, status=503)
        except Exception as e:
            logger.error("=" * 80)
            logger.error("ChatRAG POST: ОБЩАЯ ОШИБКА")
            logger.error("=" * 80)
            logger.error(f"ChatRAG POST: Тип ошибки: {type(e).__name__}")
            logger.error(f"ChatRAG POST: Сообщение: {str(e)}")
            logger.error(f"ChatRAG POST: Полная трассировка:", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка обработки запроса: {str(e)}'
            }, status=500)

    def handle_ollama_url_request(self, request):
        """Обработка запросов для ollama-url endpoint"""
        import logging
        logger = logging.getLogger(__name__)
        
        if request.method == 'GET':
            return self.get_ollama_url_view(request)
        elif request.method == 'POST':
            return self.post_ollama_url_view(request)
        else:
            return JsonResponse({
                'error': f'Метод {request.method} не поддерживается'
            }, status=405)

    def get_ollama_url_view(self, request):
        """Получить текущий Ollama URL"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            ollama_url = self.get_ollama_url()
            logger.info(f"GET ollama-url: возвращаем URL: {ollama_url}")
            
            return JsonResponse({
                'ollama_url': ollama_url
            })
        except Exception as e:
            logger.error(f"GET ollama-url: ошибка: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка получения Ollama URL: {str(e)}'
            }, status=500)

    def post_ollama_url_view(self, request):
        """Сохранить новый Ollama URL"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            ollama_url = request.data.get('ollama_url', '').strip()
            
            if not ollama_url:
                return JsonResponse({
                    'error': 'URL не может быть пустым'
                }, status=400)
            
            # Валидация формата URL
            from urllib.parse import urlparse
            try:
                parsed = urlparse(ollama_url)
                if not (parsed.scheme in ['http', 'https'] and parsed.netloc):
                    raise ValueError("Неверный формат URL")
            except Exception as e:
                return JsonResponse({
                    'error': f'Неверный формат URL: {str(e)}'
                }, status=400)
            
            # Сохраняем URL в SysOption
            sys_option, created = SysOption.objects.update_or_create(
                name='ollama_url',
                defaults={
                    'value': ollama_url,
                    'desc': 'URL сервера Ollama для подключения к моделям',
                    'category': 'ai',
                    'enabled': True,
                    'user': request.user if request.user.is_authenticated else None
                }
            )
            
            action = 'создана' if created else 'обновлена'
            logger.info(f"POST ollama-url: SysOption ollama_url {action}: {ollama_url}")
            
            return JsonResponse({
                'message': f'URL успешно {action}',
                'ollama_url': ollama_url,
                'created': created
            })
            
        except Exception as e:
            logger.error(f"POST ollama-url: ошибка: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': f'Ошибка сохранения Ollama URL: {str(e)}'
            }, status=500)
    
    def get_proxies(self, url):
        """Получить настройки прокси с обходом для локальных адресов"""
        import os
        import logging
        from urllib.parse import urlparse
        
        logger = logging.getLogger(__name__)
        
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            
            # Список локальных адресов, для которых не нужен прокси
            no_proxy_hosts = [
                'localhost',
                '127.0.0.1',
                '::1',
                '0.0.0.0'
            ]
            
            # Проверяем, является ли адрес локальным или внутренним
            is_local = (
                hostname in no_proxy_hosts or
                hostname.startswith('192.168.') or
                hostname.startswith('10.') or
                hostname.startswith('172.16.') or
                hostname.startswith('172.17.') or
                hostname.startswith('172.18.') or
                hostname.startswith('172.19.') or
                hostname.startswith('172.20.') or
                hostname.startswith('172.21.') or
                hostname.startswith('172.22.') or
                hostname.startswith('172.23.') or
                hostname.startswith('172.24.') or
                hostname.startswith('172.25.') or
                hostname.startswith('172.26.') or
                hostname.startswith('172.27.') or
                hostname.startswith('172.28.') or
                hostname.startswith('172.29.') or
                hostname.startswith('172.30.') or
                hostname.startswith('172.31.')
            )
            
            if is_local:
                logger.info(f"Адрес {hostname} определен как локальный/внутренний, прокси не используется")
                # Возвращаем пустой словарь прокси для обхода системных настроек
                return {
                    'http': None,
                    'https': None,
                    'no_proxy': hostname
                }
            
            # Для внешних адресов используем системные настройки прокси
            http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
            https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
            
            if http_proxy or https_proxy:
                logger.info(f"Используются прокси из переменных окружения")
                return {
                    'http': http_proxy,
                    'https': https_proxy
                }
            
            # Если прокси не настроены, возвращаем None (использовать системные настройки)
            logger.info("Прокси не настроены, используются системные настройки")
            return {}
            
        except Exception as e:
            logger.error(f"Ошибка определения прокси: {str(e)}")
            # В случае ошибки не используем прокси
            return {
                'http': None,
                'https': None
            }
    
    def get_ollama_url(self):
        """Получить URL Ollama из системных параметров"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            ollama_param = SysOption.objects.filter(
                name='ollama_url',
                enabled=True
            ).first()
            
            if ollama_param and ollama_param.value:
                url = ollama_param.value.rstrip('/')
                logger.info(f"Ollama URL получен из SysOption: {url}")
                return url
            else:
                # Пытаемся получить из .env или настроек по умолчанию
                import os
                url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
                logger.info(f"Ollama URL получен из переменных окружения или по умолчанию: {url}")
                return url
                
        except Exception as e:
            logger.error(f"Ошибка получения Ollama URL: {e}", exc_info=True)
            return 'http://localhost:11434'  # URL по умолчанию
    
    def get_system_context(self):
        """Получить контекстную информацию из системы"""
        try:
            context_parts = []
            
            # Получаем общее количество параметров
            param_count = Param.objects.filter(enabled=True).count()
            context_parts.append(f"Всего параметров в системе: {param_count}")
            
            # Получаем категории параметров
            categories = Param.objects.filter(enabled=True).values('category').distinct()
            if categories:
                cat_list = [cat['category'] for cat in categories]
                context_parts.append(f"Категории параметров: {', '.join(cat_list)}")
            
            # Получаем системные опции
            sys_options_count = SysOption.objects.filter(enabled=True).count()
            context_parts.append(f"Системных опций: {sys_options_count}")
            
            # Получаем комментарии
            comments_count = Comment.objects.count()
            context_parts.append(f"Всего комментариев: {comments_count}")
            
            # Добавляем несколько примеров параметров
            sample_params = Param.objects.filter(enabled=True, public=True)[:5]
            if sample_params:
                context_parts.append("\nПримеры публичных параметров:")
                for param in sample_params:
                    context_parts.append(f"- {param.name} ({param.category}): {param.desc[:100]}...")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Ошибка получения системной информации: {str(e)}"