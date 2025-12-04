from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.db import connection


@csrf_exempt
@require_POST
def db_query(request):
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()

        if not query:
            return JsonResponse({'error': 'SQL запрос не может быть пустым'}, status=400)

        # Проверка на опасные операции (базовая защита)
        dangerous_keywords = ['drop', 'delete', 'update', 'insert', 'alter', 'create', 'truncate']
        query_lower = query.lower()

        for keyword in dangerous_keywords:
            if keyword in query_lower and 'select' not in query_lower:
                return JsonResponse({'error': 'Запрещенные операции в запросе'}, status=403)

        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                return JsonResponse({
                    'columns': columns,
                    'rows': [list(row) for row in rows]
                })
            else:
                return JsonResponse({'message': 'Запрос выполнен успешно'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)