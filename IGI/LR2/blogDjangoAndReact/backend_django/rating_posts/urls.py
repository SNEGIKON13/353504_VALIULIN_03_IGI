from django.urls import path
from django.conf.urls import url
from . import views

# Set end point for requests
app_name = 'rate_posts'
urlpatterns = [
    url(r'api/rate_posts$', views.PostRatingView.as_view(), name='rate_posts'),
]