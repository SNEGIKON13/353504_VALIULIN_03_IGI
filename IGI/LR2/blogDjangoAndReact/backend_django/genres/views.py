from .models import Genre
from rest_framework import generics
from .serializers import GenreSerializer

# Generic class-based views for genres list requests
class GenresListView(generics.ListAPIView):
    serializer_class = GenreSerializer

    """
    Querys with more than one row to serialize data
    Populate genres and posts nested
    """
    queryset = Genre.objects.filter(show_menu_list='YES')