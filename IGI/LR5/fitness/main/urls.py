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

    # Отзывы
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),    # Управление записями на услуги

]
