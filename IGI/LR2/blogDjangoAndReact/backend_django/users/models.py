from django.db import models
from genres.models import get_file_path

from django.contrib.auth.models import User

# Create your models here.

class UserProfileImage(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_profile_image'
    )

    profile_image = models.ImageField(upload_to=get_file_path)