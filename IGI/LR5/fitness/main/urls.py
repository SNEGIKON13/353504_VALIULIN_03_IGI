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
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('promos/', views.promos, name='promos'),  # Добавляем маршрут для промо-акций

    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # Услуги
    path('groups/', views.groups, name='groups'),
    path('groups/<int:pk>/enroll/', views.group_enroll, name='group_enroll'),  # Add this line

    # Отзывы
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),    # Управление записями на услуги

    # Профиль и управление группами
    path('profile/', views.profile, name='profile'),  # Changed from profile_view to profile
    path('my-classes/', views.my_classes, name='my_classes'),
    path('join-group/<int:group_id>/', views.join_group, name='join_group'),
    path('leave-group/<int:membership_id>/', views.leave_group, name='leave_group'),
    path('freeze-membership/<int:membership_id>/', views.freeze_membership, name='freeze_membership'),

    path('my-sessions/', views.my_sessions, name='my_sessions'),

    # Управление занятиями
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/edit/', views.session_edit, name='session_edit'),
    path('sessions/<int:pk>/delete/', views.session_delete, name='session_delete'),

]
