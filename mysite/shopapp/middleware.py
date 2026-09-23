from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone


request_history = {}

REQUEST_LIMIT = 10
TIME_WINDOW = 60

SHOP_PREFIX = '/shop/'


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(SHOP_PREFIX):
            return self.get_response(request)

        ip = self.get_client_ip(request)
        now = timezone.now()

        if ip in request_history:
            recent_requests = [
                request_time
                for request_time in request_history[ip]
                if now - request_time < timedelta(
                    seconds=TIME_WINDOW,
                )
            ]

            if len(recent_requests) >= REQUEST_LIMIT:
                return HttpResponse(
                    'Request limit exceeded. Try again later.',
                    status=429,
                )

            request_history[ip] = recent_requests
            request_history[ip].append(now)
        else:
            request_history[ip] = [now]

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get(
            'HTTP_X_FORWARDED_FOR',
        )

        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR')