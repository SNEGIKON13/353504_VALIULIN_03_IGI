from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
import uuid
import os
from genres.models import Genre, get_file_path


#Source: Model field reference https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.DateTimeField


class Post(models.Model):

    STATUS = (
        (0,"Draft"),
        (1,"Publish")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='posts')
    updated_on = models.DateTimeField(auto_now= True)

    #Field for many to many relation and set related name to serialize data with json
    genres = models.ManyToManyField(Genre,related_name='postsgen')
    content = models.TextField()
    
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    url_website = models.URLField(max_length=200, null=True, blank=True)
    url_video = models.URLField(max_length=200, null=True, blank=True)
    director = models.CharField(max_length=200, null=True, blank=True)

    #Field from django_countries library to get a list of countries and associate the post with it
    country = CountryField()
    
    image_post = models.ImageField(upload_to=get_file_path)

    #Date fields for featured posts
    initial_featured_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_featured_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    #Field for one to many relation and set related name to serialize data with json
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='imageps')
    image_post = models.ImageField(upload_to=get_file_path)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.post.title

# Round to the nearest integer
# https://stackoverflow.com/a/35945471
class Round(models.Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'