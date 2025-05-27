from django.utils import timezone
import pytz
from django.conf import settings
import requests

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def get_timezone_from_ip(self, ip):
        try:
            api_url = f'http://ip-api.com/json/{ip}'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success' and data.get('timezone'):
                    return data['timezone']
        except:
            pass
        return settings.TIME_ZONE
    
    def __call__(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            timezone_str = self.get_timezone_from_ip(ip)
            if timezone_str:
                timezone.activate(pytz.timezone(timezone_str))
                request.session['user_timezone'] = timezone_str
        except:
            timezone.activate(pytz.timezone(settings.TIME_ZONE))
        
        response = self.get_response(request)
        return response

    def __del__(self):
        if self.reader:
            self.reader.close()
