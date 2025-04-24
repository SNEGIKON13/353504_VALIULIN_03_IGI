from django.urls import path
from django.conf.urls import url
from . import views

# Simple jwt authentication Django rest framework
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Set end point for requests
app_name = 'users'
urlpatterns = [
    url(r'api/users', views.RegisterUserView.as_view(), name='users'),
    url(r'api/update_user/(?P<pk>\d+)/$', views.UpdateUserView.as_view(), name='update_user'),
    url(r'api/profile_images$', views.ProfileImagesListView.as_view(), name='profile_images'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]