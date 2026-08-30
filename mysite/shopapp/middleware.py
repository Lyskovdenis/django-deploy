from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

# Хранилище для IP-адресов и времени последнего запроса
request_history = {}

# Лимиты
REQUEST_LIMIT = 10  # количество запросов
TIME_WINDOW = 60  # временное окно в секундах


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем IP-адрес пользователя
        ip = self.get_client_ip(request)

        # Получаем текущее время
        now = timezone.now()

        # Проверяем историю запросов для этого IP
        if ip in request_history:
            # Фильтруем запросы за последнее время
            recent_requests = [
                req_time for req_time in request_history[ip]
                if now - req_time < timedelta(seconds=TIME_WINDOW)
            ]

            # Если запросов больше лимита
            if len(recent_requests) >= REQUEST_LIMIT:
                response = HttpResponse('Превышен лимит запросов! Попробуйте позже.')
                response.status_code = 429  # Too Many Requests
                return response

            # Обновляем историю
            request_history[ip] = recent_requests
            request_history[ip].append(now)
        else:
            # Первый запрос с этого IP
            request_history[ip] = [now]

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Получение IP-адреса клиента из request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip