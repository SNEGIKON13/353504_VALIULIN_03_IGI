from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, F, Q
from django.utils import timezone
import json
from datetime import datetime
from .models import CustomUser, Service, Group, Session, Membership, ServiceBooking
from datetime import datetime
from .models import Article, About, FAQ, Staff, Vacancy, Review, Promo, Service, Group, Session, Membership, CustomUser, ServiceBooking
from .forms import CustomUserCreationForm
import requests
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F, Q
from django.db.models.functions import ExtractMonth
from datetime import timedelta
import io
import base64
import json

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
    # Для всех пользователей показываем только последнюю новость
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
    
    return render(request, 'main/home.html', context)

def news(request): # список новостей
    articles = Article.objects.all()
    return render(request, 'main/news.html', {'articles': articles})

def about(request): # о компании
    company_info = About.objects.first()  # Changed from CompanyInfo to About
    return render(request, 'main/about.html', {'company_info': company_info})

def privacy_policy(request): # политика конфиденциальности
    return render(request, 'main/privacy_policy.html')

def faq(request): # вопросы-ответы
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})

def staff(request): # контакты сотрудников
    staff_members = Staff.objects.all()
    return render(request, 'main/staff.html', {'staff_members': staff_members})

def vacancies(request): # вакансии
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'main/vacancies.html', {'vacancies': vacancies_list})

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

    return render(request, 'main/reviews.html', {
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
    return render(request, 'main/promos.html', {
        'active_promos': active_promos,
        'archived_promos': archived_promos
    })

@login_required
def review_list(request):
    user_reviews = Review.objects.filter(name=request.user.get_full_name() or request.user.username)
    all_reviews = Review.objects.filter(is_approved=True)
    return render(request, 'main/reviews/list.html', {
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
    return render(request, 'main/reviews/form.html')

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
    return render(request, 'main/reviews/form.html', {'review': review})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, name=request.user.get_full_name() or request.user.username)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв успешно удален')
        return redirect('main:review_list')
    return render(request, 'main/reviews/delete.html', {'review': review})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:home')

def is_instructor(user):
    return user.is_instructor

@login_required
def profile(request):
    if request.user.is_instructor:
        # Для инструктора
        instructor_groups = Group.objects.filter(instructors=request.user)
        upcoming_sessions = Session.objects.filter(
            instructors=request.user,
            start_time__gte=timezone.now()
        ).order_by('start_time')
        return render(request, 'main/profile_instructor.html', {
            'groups': instructor_groups,
            'sessions': upcoming_sessions
        })
    else:
        # Для клиента
        active_memberships = Membership.objects.filter(
            user=request.user,
            status='active'
        )
        available_services = Service.objects.all()
        total_spent = Membership.objects.filter(
            user=request.user
        ).aggregate(total=Sum('payment_amount'))['total'] or 0
        return render(request, 'main/profile_client.html', {
            'memberships': active_memberships,
            'services': available_services,
            'total_spent': total_spent
        })

@login_required
def purchase_membership(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        # Проверка наличия мест в группе
        current_members = Membership.objects.filter(group=group, status='active').count()
        if current_members >= group.max_participants:
            messages.error(request, 'Группа уже заполнена')
            return redirect('main:profile')
            
        # Создание членства
        Membership.objects.create(
            user=request.user,
            group=group,
            start_date=group.start_date,
            end_date=group.end_date,
            payment_amount=group.price,
            payment_date=timezone.now().date(),
            status='active'
        )
        messages.success(request, 'Вы успешно записались в группу')
        return redirect('main:profile')
    return render(request, 'main/purchase_membership.html', {'group': group})

@login_required
@user_passes_test(is_instructor)
def instructor_schedule(request):
    upcoming_sessions = Session.objects.filter(
        instructors=request.user,
        start_time__gte=timezone.now()
    ).order_by('start_time')
    return render(request, 'main/instructor_schedule.html', {
        'sessions': upcoming_sessions
    })

def service_list(request):
    # Make services visible for all users
    services = Service.objects.all()
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)
        
    # Sort by price or name
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        services = services.order_by('price')
    elif sort_by == 'price_desc':
        services = services.order_by('-price')
    elif sort_by == 'name':
        services = services.order_by('name')
    
    return render(request, 'main/services/list.html', {
        'services': services,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by
    })

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    groups = Group.objects.filter(service=service)
    return render(request, 'main/services/detail.html', {
        'service': service,
        'groups': groups
    })

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'main/groups/groups_list.html', {'groups': groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'main/groups/detail.html', {'group': group})

@login_required
def user_purchases(request):
    memberships = Membership.objects.filter(user=request.user)
    return render(request, 'main/profile/purchases.html', {'memberships': memberships})

@login_required
def instructor_groups(request):
    if not request.user.is_instructor:
        messages.error(request, 'Доступ запрещен')
        return redirect('main:home')
    groups = Group.objects.filter(instructors=request.user)
    return render(request, 'main/instructor/groups.html', {'groups': groups})

@login_required
def booking_list(request):
    bookings = ServiceBooking.objects.filter(user=request.user).select_related('service').order_by('-created_at')
    return render(request, 'main/services/booking_list.html', {'bookings': bookings})

@login_required
def booking_edit(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id, user=request.user)
    if request.method == 'POST':
        try:
            preferred_date = timezone.make_aware(datetime.strptime(
                request.POST.get('preferred_date'),
                '%Y-%m-%dT%H:%M'
            ))
            booking.preferred_date = preferred_date
            booking.notes = request.POST.get('notes', '')
            booking.status = 'pending'  # Reset status to pending after edit
            booking.save()
            messages.success(request, 'Запись успешно обновлена')
            return redirect('main:my_bookings')
        except ValueError:
            messages.error(request, 'Неверный формат даты')
    return render(request, 'main/services/booking_form.html', {
        'booking': booking,
        'service': booking.service
    })

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Запись отменена')
        return redirect('main:my_bookings')
    return render(request, 'main/services/booking_cancel.html', {'booking': booking})

@login_required
def service_book(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        try:
            preferred_date = timezone.make_aware(datetime.strptime(
                request.POST.get('preferred_date'),
                '%Y-%m-%dT%H:%M'
            ))
            
            # Validate that the preferred date is in the future
            if preferred_date <= timezone.now():
                messages.error(request, 'Дата записи должна быть в будущем')
                return render(request, 'main/services/booking_form.html', {'service': service})
                
            booking = ServiceBooking.objects.create(
                user=request.user,
                service=service,
                preferred_date=preferred_date,
                notes=request.POST.get('notes', ''),
                status='pending'
            )
            messages.success(request, 'Вы успешно записались на услугу')
            return redirect('main:my_bookings')
        except ValueError:
            messages.error(request, 'Неверный формат даты')
    return render(request, 'main/services/booking_form.html', {'service': service})

@user_passes_test(lambda u: u.is_superuser)
def admin_statistics(request):
    # Статистика по группам
    groups_stats = Group.objects.annotate(
        member_count=Count('membership'),
        occupancy_rate=F('member_count') * 100.0 / F('max_participants')
    )
    
    # Средний возраст клиентов
    users_with_age = CustomUser.objects.filter(is_instructor=False).exclude(birth_date=None)
    ages = [user.age() for user in users_with_age if user.age() is not None]
    average_age = sum(ages) / len(ages) if ages else 0
    
    # Популярные услуги
    popular_services = Service.objects.annotate(
        booking_count=Count('servicebooking')
    ).order_by('-booking_count')[:5]
    
    # Доходы по услугам
    service_revenue = Membership.objects.values(
        'group__service__name'
    ).annotate(
        total_revenue=Sum('payment_amount')
    ).order_by('-total_revenue')
    
    # Статистика посещаемости
    attendance_stats = Session.objects.annotate(
        attendance_count=Count('attendance', filter=Q(attendance__attended=True)),
        total_members=Count('group__membership'),
        attendance_rate=F('attendance_count') * 100.0 / F('total_members')
    )
    
    # Данные для графика
    attendance_data = {
        'labels': [session.start_time.strftime('%d/%m/%Y') for session in attendance_stats],
        'data': [float(session.attendance_rate) for session in attendance_stats]
    }
    
    context = {
        'groups_stats': groups_stats,
        'average_age': round(average_age, 1),
        'popular_services': popular_services,
        'service_revenue': service_revenue,
        'attendance_stats': attendance_stats,
        'attendance_data': json.dumps(attendance_data)
    }
    
    return render(request, 'main/admin/statistics.html', context)

def list_groups(request):
    return render(request, 'main/groups_list.html')