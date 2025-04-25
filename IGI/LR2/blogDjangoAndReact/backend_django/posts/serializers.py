from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Image
from genres.models import Genre

#Serialize Image nested array
class ImageSerializer(serializers.ModelSerializer):
    #Set alias for field. Source: https://stackoverflow.com/a/43492545/9655579
    title = serializers.CharField(source='name')

    class Meta:
        model = Image
        fields = ['id','image_post','title','description']

class GenrePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')

class PostSerializer(serializers.ModelSerializer):
    
    #Put genres data inside postsgen as a nested array
    genres = GenrePostSerializer(read_only=True,many=True)

    #Put images data inside postsgen as a nested array
    imageps = ImageSerializer(read_only=True,many=True)

    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'title',
                  'slug',
                  'description',
                  'author',
                  'updated_on',
                  'genres',
                  'content',
                  'created_on',
                  'status',
                  'url_website',
                  'url_video',
                  'director',
                  'country',
                  'image_post',
                  'imageps',
                  'avg_rating']
