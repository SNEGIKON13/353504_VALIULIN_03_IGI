from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PostRating
from genres.models import Genre


#Serialize rating
class PostRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostRating
        fields = ['post',
                  'author',
                  'rating']

    # Validate post request data
    # https://stackoverflow.com/a/59468176
    def validate(self, data):
        """
        Check if register exists
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#exists
        """
        if PostRating.objects.filter(post=data['post'], author=data['author']).exists():
            raise serializers.ValidationError("You have already rated this post")

        return data