from functools import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, F, Q, Case, When, Value, FloatField, Avg
from django.utils import timezone
from datetime import datetime
from .models import Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser, Group, Membership, Attendance
from .forms import CustomUserCreationForm
import requests
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import timedelta
import json
import pytz
from calendar import monthcalendar
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
import io
import base64
from .decorators import api_auth_required, api_rate_limit
from django.core.cache import cache
from statistics import StatisticsError, mode

def get_random_quote():
    default_quote = {"quote": "Мудрость приходит со временем", "author": "Народная мудрость"}
    try:
        response = requests.get('https://zenquotes.io/api/random', timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {"quote": data[0]['q'], "author": data[0]['a']}
    except (requests.RequestException, KeyError, ValueError, IndexError):
        pass
    return default_quote

def get_daily_advice():
    default_advice = "Никогда не сдавайся!"
    try:
        response = requests.get('https://api.adviceslip.com/advice', timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'slip' in data and 'advice' in data['slip']:
                return data['slip']['advice']
    except (requests.RequestException, KeyError, ValueError):
        pass
    return default_advice

def home(request): # главная со статьей
    latest_article = Article.objects.first()
    context = {
        'article': latest_article,
    }
    
    # Для авторизованных пользователей добавляем цитату и совет
    if request.user.is_authenticated:
        quote_data = get_random_quote()  # Now guaranteed to return a valid dict
        advice = get_daily_advice()      # Now guaranteed to return a string
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

@api_auth_required
@api_rate_limit(calls=100, period=3600)
@login_required
def reviews(request): # отзывы
    reviews_list = Review.objects.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_staff:
            messages.error(request, 'Администраторы не могут оставлять отзывы')
            return redirect('main:reviews')
            
        Review.objects.create(
            name=request.user.get_full_name() or request.user.username,
            rating=request.POST.get('rating'),
            text=request.POST.get('text')
        )
        return redirect('main:reviews')

    return render(request, 'reviews.html', {
        'reviews': reviews_list
    })

@api_auth_required
@api_rate_limit(calls=50, period=3600)
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

@api_auth_required
@api_rate_limit(calls=100, period=3600)
def groups(request, year=None, month=None, min_price=None, max_price=None, min_duration=None, max_duration=None):
    # Поскольку декоратор уже проверяет аутентификацию, 
    # мы можем быть уверены что request.user существует
    groups_list = Group.objects.filter(is_active=True)
    
    # Фильтрация по дате
    if year and month:
        groups_list = groups_list.filter(start_date__year=year, start_date__month=month)
    
    # Фильтрация по цене
    if min_price and max_price:
        groups_list = groups_list.filter(price__range=(min_price, max_price))
        
    # Фильтрация по длительности
    if min_duration and max_duration:
        groups_list = groups_list.filter(duration__range=(min_duration, max_duration))
    
    # Остальной код view остается без изменений
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
    
    # Подсчет оставшихся запросов (без ошибки, только для неавторизованных)
    api_requests_remaining = None
    if not request.user.is_authenticated:
        client_ip = request.META.get('REMOTE_ADDR')
        cache_key = f"ratelimit_{client_ip}"
        calls_history = cache.get(cache_key, [])
        api_requests_remaining = 100 - len(calls_history)
    
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
    
    # Сортируем данные календаря по дате
    calendar_data = dict(sorted(calendar_data.items()))
    
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
    
    context = {
        'groups': groups_list,
        'current_sort': sort_by,
        'calendar_data': calendar_data,
        'current_time': local_time,
        'calendar_weeks': calendar_weeks,
        'api_requests_remaining': api_requests_remaining,
    }
    
    return render(request, 'groups.html', context)

@login_required
def profile(request):
    if request.user.is_staff:
        return redirect('admin:index')  # Перенаправляем админа в админку
    
    context = {'user': request.user}
    
    if request.user.is_instructor:
        # Instructor view
        instructor_groups = Group.objects.filter(instructors=request.user)
        upcoming_sessions = []
        
        # Get next 30 days of sessions
        today = timezone.now().date()
        thirty_days = today + timedelta(days=30)
        
        for group in instructor_groups:
            for date in group.get_schedule_dates():
                if today <= date <= thirty_days:
                    upcoming_sessions.append({
                        'group': group,
                        'date': date,
                        'attendees': group.members.count()
                    })
        
        # Sort sessions and remove duplicates
        upcoming_sessions = sorted(upcoming_sessions, key=lambda x: (x['date'], x['group'].name))
        
        context.update({
            'is_instructor': True,
            'instructor_groups': instructor_groups.distinct(),
            'upcoming_sessions': upcoming_sessions
        })
        return render(request, 'profile_instructor.html', context)
    else:
        # Regular user view
        memberships = Membership.objects.filter(user=request.user).select_related('group').prefetch_related('group__instructors')
        attendances = Attendance.objects.filter(
            user=request.user
        ).select_related('group').prefetch_related('group__instructors').order_by('-session_date')
        
        context.update({
            'is_instructor': False,
            'memberships': memberships,
            'attendances': attendances
        })
        return render(request, 'profile.html', context)

@login_required
def my_classes(request):
    memberships = Membership.objects.filter(user=request.user).select_related('group')
    return render(request, 'my_classes.html', {'memberships': memberships})

@login_required
def join_group(request, group_id):
    # Prevent instructors from enrolling
    if request.user.is_instructor:
        messages.error(request, 'Инструкторы не могут записываться на занятия')
        return redirect('main:groups')
        
    group = get_object_or_404(Group, id=group_id, is_active=True)
    
    if group.available_spots <= 0:
        messages.error(request, 'В группе нет свободных мест')
        return redirect('main:groups')
        
    if Membership.objects.filter(user=request.user, group=group).exists():
        messages.warning(request, 'Вы уже записаны в эту группу')
        return redirect('main:my_classes')
    
    Membership.objects.create(user=request.user, group=group)
    messages.success(request, f'Вы успешно записались в группу {group.name}')
    return redirect('main:my_classes')

@login_required
def leave_group(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, user=request.user)
    
    if request.method == 'POST':
        membership.delete()
        messages.success(request, f'Вы покинули группу {membership.group.name}')
        return redirect('main:my_classes')
    
    return render(request, 'confirm_leave_group.html', {'membership': membership})

@login_required
def freeze_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, user=request.user)
    
    if membership.status == 'active':
        membership.status = 'frozen'
        messages.success(request, 'Абонемент заморожен')
    elif membership.status == 'frozen':
        membership.status = 'active'
        messages.success(request, 'Абонемент активирован')
        
    membership.save()
    return redirect('main:my_classes')

@login_required
def my_sessions(request):
    # Get all user's memberships
    memberships = Membership.objects.filter(user=request.user)
    
    # Get schedule for each group
    sessions = []
    for membership in memberships:
        group = membership.group
        dates = group.get_schedule_dates()
        for date in dates:
            attendance = Attendance.objects.filter(
                user=request.user,
                group=group,
                session_date=date
            ).first()
            
            sessions.append({
                'group': group,
                'date': date,
                'start_time': group.start_time,
                'end_time': group.end_time,
                'instructors': group.instructors.all(),
                'attended': attendance.attended if attendance else False
            })
    
    # Sort sessions by date and time
    sessions.sort(key=lambda x: (x['date'], x['start_time']))
    
    return render(request, 'sessions.html', {
        'sessions': sessions
    })

@login_required
def group_enroll(request, pk):
    # Prevent instructors from enrolling
    if request.user.is_instructor:
        messages.error(request, 'Инструкторы не могут записываться на занятия')
        return redirect('main:groups')
        
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        # Check if user is already enrolled
        if Membership.objects.filter(user=request.user, group=group).exists():
            messages.warning(request, f'Вы уже записаны в группу {group.name}')
            return redirect('main:groups')
            
        if group.available_spots > 0:
            # Create membership
            Membership.objects.create(
                user=request.user,
                group=group,
                status='active'
            )
            messages.success(request, f'Вы успешно записались в группу {group.name}')
        else:
            messages.error(request, 'В группе нет свободных мест')
    
    return redirect('main:groups')

@login_required
def session_create(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        session_date = request.POST.get('date')
        
        group = get_object_or_404(Group, id=group_id)
        
        # Check if user is already a member
        if not Membership.objects.filter(user=request.user, group=group).exists():
            messages.error(request, 'Вы не являетесь участником этой группы')
            return redirect('main:profile')
            
        # Check if attendance already exists
        if Attendance.objects.filter(user=request.user, group=group, session_date=session_date).exists():
            messages.error(request, 'Вы уже записаны на это занятие')
            return redirect('main:profile')
            
        Attendance.objects.create(
            user=request.user,
            group=group,
            session_date=session_date
        )
        messages.success(request, 'Вы успешно записались на занятие')
        return redirect('main:profile')
        
    groups = request.user.member_groups.all()
    return render(request, 'sessions/create.html', {'groups': groups})

@login_required
def session_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    
    if request.method == 'POST':
        attendance.session_date = request.POST.get('date')
        attendance.save()
        messages.success(request, 'Запись на занятие обновлена')
        return redirect('main:profile')
        
    return render(request, 'sessions/edit.html', {'attendance': attendance})

@login_required
def session_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Запись на занятие отменена')
        return redirect('main:profile')
        
    return render(request, 'sessions/delete.html', {'attendance': attendance})

def is_regular_user(user):
    return user.is_authenticated and not user.is_staff and not user.is_instructor

def is_instructor(user):
    return user.is_authenticated and user.is_instructor

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_statistics(request):
    # Get filter parameters and set defaults
    selected_group = request.GET.get('group')
    start_date = request.GET.get('start_date') or (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = request.GET.get('end_date') or timezone.now().strftime('%Y-%m-%d')
    
    # Base queries
    clients = CustomUser.objects.filter(is_instructor=False, is_staff=False).order_by('username')
    groups = Group.objects.all()
    
    # Memberships with date filter
    memberships = Membership.objects.filter(
        date_joined__date__range=(start_date, end_date)
    )
    if selected_group:
        memberships = memberships.filter(group_id=selected_group)

    # Total revenue and active clients
    total_revenue = memberships.aggregate(total=Sum('group__price'))['total'] or 0
    total_active_clients = clients.filter(memberships__status='active').distinct().count()

    # Client statistics with spending
    clients_with_stats = clients.annotate(
        total_spent=Sum('memberships__group__price'),
        groups_count=Count('memberships', distinct=True)
    ).order_by('username')

    # Calculate spending statistics
    all_spendings = [c.total_spent or 0 for c in clients_with_stats]
    spending_stats = {
        'avg': sum(all_spendings) / len(all_spendings) if all_spendings else 0,
        'median': sorted(all_spendings)[len(all_spendings)//2] if all_spendings else 0
    }
    try:
        spending_stats['mode'] = mode(all_spendings)
    except StatisticsError:
        spending_stats['mode'] = all_spendings[0] if all_spendings else 0

    # Age statistics
    ages = [c.age() for c in clients if c.age()]
    age_stats = {
        'avg': sum(ages) / len(ages) if ages else 0,
        'median': sorted(ages)[len(ages)//2] if ages else 0
    }

    # Group statistics
    groups_stats = []
    for group in groups:
        # Count active members through Membership model
        member_count = Membership.objects.filter(
            group=group,
            status='active'
        ).count()

        # Calculate actual revenue from active memberships
        revenue = group.price * member_count

        # Count sessions in the date range
        session_count = 0
        if start_date and end_date:
            session_dates = set()  # Use set to avoid duplicate dates
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            for date in group.get_all_session_dates():  # We'll add this method to Group model
                if start <= date <= end:
                    session_dates.add(date)
            session_count = len(session_dates)
        
        # Get all members for this group through Membership
        members = CustomUser.objects.filter(
            memberships__group=group,
            memberships__status='active'
        ).values('username')
        
        group_data = {
            'name': group.name,
            'member_count': member_count,
            'revenue': revenue,
            'sessions': session_count,
            'members': members  # Only contains usernames now
        }
        groups_stats.append(group_data)

    # Sort groups by revenue for plot
    groups_stats.sort(key=lambda x: x['revenue'], reverse=True)
    
    # Create revenue plot
    plt.figure(figsize=(12, 6))
    plt.bar(
        [g['name'] for g in groups_stats[:10]],
        [float(g['revenue']) for g in groups_stats[:10]]
    )
    plt.xticks(rotation=45, ha='right')
    plt.title('Топ-10 групп по доходности')
    plt.ylabel('Доход (руб.)')
    plt.tight_layout()

    # Save plot
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    revenue_plot = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    context = {
        'clients': clients_with_stats,
        'total_revenue': total_revenue,
        'total_active_clients': total_active_clients,
        'spending_stats': spending_stats,
        'age_stats': age_stats,
        'groups_stats': groups_stats[:10],  # Top 10 groups
        'revenue_plot': revenue_plot,
        'selected_group': selected_group,
        'start_date': start_date,
        'end_date': end_date,
        'groups': groups
    }

    return render(request, 'admin/statistics.html', context)

def instructor_profile(request, username):
    """View for displaying instructor's profile and their groups"""
    instructor = get_object_or_404(CustomUser, username=username, is_instructor=True)
    
    # Get instructor's groups
    groups = Group.objects.filter(instructors=instructor, is_active=True)
    
    # Get upcoming sessions for next 30 days
    today = timezone.now().date()
    thirty_days = today + timedelta(days=30)
    
    upcoming_sessions = []
    for group in groups:
        for date in group.get_schedule_dates():
            if today <= date <= thirty_days:
                upcoming_sessions.append({
                    'group': group,
                    'date': date,
                    'attendees': group.members.count()
                })
    
    # Sort sessions by date
    upcoming_sessions.sort(key=lambda x: x['date'])
    
    context = {
        'instructor': instructor,
        'groups': groups,
        'upcoming_sessions': upcoming_sessions
    }
    
    return render(request, 'instructor_profile.html', context)

def reviews_by_rating(request, rating):
    """View for filtering reviews by rating"""
    rating = int(rating)  # Convert string to integer
    reviews_list = Review.objects.filter(rating=rating)
    return render(request, 'reviews.html', {
        'reviews': reviews_list,
        'current_rating': rating
    })



