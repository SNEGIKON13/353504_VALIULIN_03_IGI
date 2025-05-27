from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('staff/', views.staff, name='staff'),
    
    # Статистика для администратора
    path('admin/statistics/', views.admin_statistics, name='admin_statistics'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('promos/', views.promos, name='promos'),  # Добавляем маршрут для промо-акций

    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Услуги и группы
    path('services/<int:service_id>/book/', views.service_book, name='service_book'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('services/', views.service_list, name='services'),
    path('groups/', views.group_list, name='groups_list'),  # изменено с 'groups' на 'groups_list'
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('purchase/<int:group_id>/', views.purchase_membership, name='purchase_membership'),

    # Личный кабинет
    path('profile/', views.profile, name='profile'),
    path('profile/purchases/', views.user_purchases, name='user_purchases'),

    # Инструкторский раздел
    path('instructor/schedule/', views.instructor_schedule, name='instructor_schedule'),
    path('instructor/groups/', views.instructor_groups, name='instructor_groups'),

    # Отзывы
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),    # Управление записями на услуги
    path('bookings/', views.booking_list, name='my_bookings'),
    path('bookings/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),

    # Административная статистика
    path('admin/statistics/', views.admin_statistics, name='admin_statistics'),
]
