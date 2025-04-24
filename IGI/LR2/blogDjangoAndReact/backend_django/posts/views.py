from django.http.response import JsonResponse
 
from .models import Post, Image, Round

from .serializers import (
    PostSerializer,
)

from datetime import datetime

from rest_framework.parsers import JSONParser
from rest_framework import status, generics, permissions


from django.db.models import Avg, F

# Class-based Views
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views

"""
Applying inheritance to classes
"""

# Generic class-based views for genres list requests

# Generic class-based views for posts list requests
class PostsListView(generics.ListAPIView):
    serializer_class = PostSerializer

    """
    Querys with more than one row to serialize data
    Populate posts and images nested
    
    Calculate average of rating and round to the nearest integer
    https://stackoverflow.com/a/51645709
    """
    queryset = Post.objects.filter(
        status='1'
    ).order_by('-created_on').annotate(
        avg_rating=Round(Avg(F('ratingps__rating')))
    )

    # https://docs.djangoproject.com/en/3.2/ref/models/expressions/#subquery-expressions
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#expressions-can-reference-transforms

# Generic class-based views forFeatured  posts list requests
class FeaturedPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Querys with more than one row to serialize data
        Populate posts and images nested
        """
        # Current date and time
        current_date = datetime.now()
        
        # Filter featured posts: current datetime between datetimes fields in the database
        post = Post.objects.filter(status='1', initial_featured_date__lte = current_date, end_featured_date__gte = current_date)

        return post

