from django.db import models
from posts.serializers import Post
from django.contrib.auth.models import User
# Create your models here.

class PostRating(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='ratingps')

    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='ratingus')

    #Text that will be shown in Django Admin fields for this model
    ONE_STAR = '1'
    TWO_STARS = '2'
    THREE_STARS = '3'
    FOUR_STARS = '4'
    FIVE_STARS = '5'

    RATING_CHOICES = [
        (ONE_STAR, 'One star'),
        (TWO_STARS, 'Two stars'),
        (THREE_STARS, 'Three stars'),
        (FOUR_STARS, 'Three stars'),
        (FIVE_STARS, 'Five stars'),
    ]

    #Add data with text to the field
    rating = models.CharField(
        max_length=1,
        choices=RATING_CHOICES,
    )

    datetime = models.DateTimeField(auto_now_add=True)

