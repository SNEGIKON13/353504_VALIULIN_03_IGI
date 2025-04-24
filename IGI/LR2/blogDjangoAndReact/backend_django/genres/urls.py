from django.urls import path
from django.conf.urls import url
from . import views

# Set end point for requests
app_name = 'genres'
urlpatterns = [
    url(r'api/genres$', views.GenresListView.as_view(), name='genres'),
]