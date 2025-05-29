from django.urls import path, re_path
from . import views

app_name = 'main'

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),  # пустой путь для главной страницы
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('staff/', views.staff, name='staff'),
    
    # Статистика для администратора
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('promos/', views.promos, name='promos'),  # Добавляем маршрут для промо-акций
    path('statistics/', views.admin_statistics, name='admin_statistics'),  # Добавлен маршрут для админ. статистики

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

    # Примеры с регулярными выражениями
    re_path(r'^groups/(?P<year>\d{4})/(?P<month>\d{2})/$', views.groups, name='groups_by_date'),
    re_path(r'^groups/price/(?P<min_price>\d+)-(?P<max_price>\d+)/$', views.groups, name='groups_by_price'),
    re_path(r'^groups/duration/(?P<min_duration>\d+)-(?P<max_duration>\d+)/$', views.groups, name='groups_by_duration'),
    re_path(r'^instructor/(?P<username>[\w.@+-]+)/$', views.instructor_profile, name='instructor_profile'),
    re_path(r'^reviews/rating/(?P<rating>[1-5])/$', views.reviews_by_rating, name='reviews_by_rating'),    # URL-паттерны для CRUD операций с группами
    path('manage/groups/', views.admin_groups, name='admin_groups'),
    path('manage/groups/create/', views.admin_group_create, name='admin_group_create'),
    path('manage/groups/<int:group_id>/edit/', views.admin_group_edit, name='admin_group_edit'),
    path('manage/groups/<int:group_id>/delete/', views.admin_group_delete, name='admin_group_delete'),
]
