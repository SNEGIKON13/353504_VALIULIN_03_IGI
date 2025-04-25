from rest_framework import serializers

from .models import Genre
from posts.serializers import PostSerializer

# Parent array nested objects genres
class GenreSerializer(serializers.ModelSerializer):
    # Put post data inside genres as a nested array
    postsgen = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Genre
        fields = ['id',
                  'name',
                  'slug',
                  'description',
                  'show_menu_list',
                  'image_genre',
                  'postsgen']