from django.urls import path
from django.conf.urls import url
from . import views

# Set end point for requests
app_name = 'comments'
urlpatterns = [
    url(r'api/comments$', views.CommentsView.as_view(), name='comments'),
]