from django.urls import path
from django.conf.urls import url 
from . import views

# Set end point for requests
app_name = 'posts'
urlpatterns = [
    url(r'api/posts$', views.PostsListView.as_view(), name='posts'),
    url(r'api/featured_posts$', views.FeaturedPostsListView.as_view(), name='featured_posts'),
]