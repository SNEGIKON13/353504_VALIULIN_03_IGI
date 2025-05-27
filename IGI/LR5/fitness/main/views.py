from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, F, Q, Case, When, Value, FloatField, Case
from django.utils import timezone
from datetime import datetime
from .models import Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser, Group
from .forms import CustomUserCreationForm
import requests
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F, Q
from django.db.models.functions import ExtractMonth
from datetime import timedelta
import json
import pytz
from calendar import monthcalendar
from datetime import datetime, timedelta

def get_random_quote():
    try:
        response = requests.get('https://zenquotes.io/api/random')
        if response.status_code == 200:
            data = response.json()[0]
            return {"quote": data['q'], "author": data['a']}
    except:
        return {"quote": "Мудрость приходит со временем", "author": "Народная мудрость"}

def get_daily_advice():
    try:
        response = requests.get('https://api.adviceslip.com/advice')
        if response.status_code == 200:
            return response.json()['slip']['advice']
    except:
        return "Никогда не сдавайся!"

def home(request): # главная со статьей
    latest_article = Article.objects.first()
    context = {
        'article': latest_article,
    }
    
    # Для авторизованных пользователей добавляем цитату и совет
    if request.user.is_authenticated:
        quote_data = get_random_quote()
        advice = get_daily_advice()
        context.update({
            'quote': quote_data['quote'],
            'philosopher': quote_data['author'],
            'advice': advice,
        })
    
    return render(request, 'home.html', context)

def news(request): # список новостей
    articles = Article.objects.all()
    return render(request, 'news.html', {'articles': articles})

def about(request): # о компании
    company_info = About.objects.first()  # Changed from CompanyInfo to About
    return render(request, 'about.html', {'company_info': company_info})

def privacy_policy(request): # политика конфиденциальности
    return render(request, 'privacy_policy.html')

def faq(request): # вопросы-ответы
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def staff(request): # контакты сотрудников
    staff_members = Staff.objects.all()
    return render(request, 'staff.html', {'staff_members': staff_members})

def vacancies(request): # вакансии
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'vacancies.html', {'vacancies': vacancies_list})

@login_required
def reviews(request): # отзывы
    reviews_list = Review.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        Review.objects.create(
            name=request.user.get_full_name() or request.user.username,
            rating=request.POST.get('rating'),
            text=request.POST.get('text')
        )
        return redirect('main:reviews')

    return render(request, 'reviews.html', {
        'reviews': reviews_list
    })

def promos(request): # промокоды
    active_promos = Promo.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    archived_promos = Promo.objects.filter(
        valid_to__lt=timezone.now()
    )
    return render(request, 'promos.html', {
        'active_promos': active_promos,
        'archived_promos': archived_promos
    })

@login_required
def review_list(request):
    user_reviews = Review.objects.filter(name=request.user.get_full_name() or request.user.username)
    all_reviews = Review.objects.filter(is_approved=True)
    return render(request, 'reviews/list.html', {
        'user_reviews': user_reviews,
        'all_reviews': all_reviews
    })

@login_required
def review_create(request):
    if request.method == 'POST':
        Review.objects.create(
            name=request.user.get_full_name() or request.user.username,
            rating=request.POST.get('rating'),
            text=request.POST.get('text')
        )
        messages.success(request, 'Отзыв успешно добавлен и ожидает модерации')
        return redirect('main:reviews')
    return render(request, 'reviews/form.html')

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk, name=request.user.get_full_name() or request.user.username)
    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.text = request.POST.get('text')
        review.is_approved = False
        review.save()
        messages.success(request, 'Отзыв успешно обновлен и ожидает модерации')
        return redirect('main:review_list')
    return render(request, 'reviews/form.html', {'review': review})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, name=request.user.get_full_name() or request.user.username)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв успешно удален')
        return redirect('main:review_list')
    return render(request, 'reviews/delete.html', {'review': review})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:home')

def groups(request):
    groups_list = Group.objects.filter(is_active=True)
    
    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        groups_list = groups_list.order_by('price')
    elif sort_by == 'price_desc':
        groups_list = groups_list.order_by('-price')
    elif sort_by == 'duration_asc':
        groups_list = groups_list.order_by('duration')
    elif sort_by == 'duration_desc':
        groups_list = groups_list.order_by('-duration')
    
    # Получаем текущее время в UTC
    now = timezone.now()
    local_tz = pytz.timezone('Europe/Minsk')
    local_time = now.astimezone(local_tz)
    
    # Подготавливаем данные для календаря
    calendar_data = {}
    for group in groups_list:
        for date in group.get_schedule_dates():
            if date not in calendar_data:
                calendar_data[date] = []
            calendar_data[date].append({
                'name': group.name,
                'start_time': group.start_time,
                'end_time': group.end_time,
                'available_spots': group.available_spots
            })
    
    # Подготовка календаря
    today = timezone.now().date()
    cal = monthcalendar(today.year, today.month)
    calendar_weeks = []
    
    for week in cal:
        week_data = []
        for day_num in week:
            if day_num != 0:
                current_date = datetime(today.year, today.month, day_num).date()
                day_events = []
                for group in groups_list:
                    if current_date in group.get_schedule_dates():
                        day_events.append({
                            'name': group.name,
                            'start_time': group.start_time,
                            'end_time': group.end_time,
                        })
                week_data.append(({"day": day_num, "date": current_date}, day_events))
            else:
                week_data.append(({"day": 0, "date": None}, []))
        calendar_weeks.append(week_data)
    
    return render(request, 'groups.html', {
        'groups': groups_list,
        'current_sort': sort_by,
        'calendar_data': calendar_data,
        'current_time': local_time,
        'calendar_weeks': calendar_weeks,
    })



