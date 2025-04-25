
from .models import PostRating

from .serializers import (
    PostRatingSerializer,
)
from rest_framework import status, generics, permissions


from django.db.models import Avg, F

class PostRatingView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostRatingSerializer
    queryset = PostRating.objects.all()

    """
    IsAuthenticatedOrReadOnly
    https://www.django-rest-framework.org/api-guide/permissions/#isauthenticatedorreadonly
    """

from django.shortcuts import render

# Create your views here.
