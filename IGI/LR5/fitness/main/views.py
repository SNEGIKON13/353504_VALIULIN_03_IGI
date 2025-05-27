from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, F, Q, Case, When, Value, FloatField, Case
from django.utils import timezone
from datetime import datetime
from .models import Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser, Group, Membership, Attendance
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

@login_required
def profile(request):
    context = {'user': request.user}
    
    if request.user.is_instructor:
        # Instructor view
        instructor_groups = Group.objects.filter(instructors=request.user)
        upcoming_sessions = []
        
        for group in instructor_groups:
            for date in group.get_schedule_dates():
                if date >= timezone.now().date():
                    upcoming_sessions.append({
                        'group': group,
                        'date': date,
                        'attendees': group.members.count()
                    })
        
        context.update({
            'is_instructor': True,
            'instructor_groups': instructor_groups,
            'upcoming_sessions': sorted(upcoming_sessions, key=lambda x: x['date'])
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



