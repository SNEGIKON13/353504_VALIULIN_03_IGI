from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.cache import cache
import time

def api_auth_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Проверяем, является ли запрос API запросом
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'error': 'Authentication required',
                    'status': 401
                }, status=401)
            # Для обычных запросов - редирект на логин
            return redirect('main:login')
        return view_func(request, *args, **kwargs)
    return wrapped

def api_rate_limit(calls=100, period=3600):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                client_ip = request.META.get('REMOTE_ADDR')
            else:
                client_ip = f"user_{request.user.id}"
                
            cache_key = f"ratelimit_{client_ip}"
            calls_history = cache.get(cache_key, [])
            current_time = time.time()
            
            # Очищаем историю от старых вызовов
            calls_history = [x for x in calls_history if current_time - x < period]
            
            if len(calls_history) >= calls:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'status': 429
                }, status=429)
                
            calls_history.append(current_time)
            cache.set(cache_key, calls_history, period)
            
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
