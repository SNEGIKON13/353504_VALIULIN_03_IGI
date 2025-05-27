import calendar
from datetime import datetime
import pytz
from django.utils import timezone

def get_text_calendar(year=None, month=None, locale='ru_RU'):
    """Generate a text calendar for the given month and year"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
        
    # Set locale for month names
    cal = calendar.LocaleTextCalendar(locale=locale)
    return cal.formatmonth(year, month)

def format_date(date):
    """Format date in DD/MM/YYYY format"""
    if date:
        return date.strftime("%d/%m/%Y")
    return ""

def format_datetime(dt):
    """Format datetime in DD/MM/YYYY HH:MM format with timezone"""
    if dt:
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        local_dt = timezone.localtime(dt)
        return {
            'formatted': local_dt.strftime("%d/%m/%Y %H:%M"),
            'timezone': local_dt.tzinfo.zone
        }
    return {'formatted': "", 'timezone': ""}
