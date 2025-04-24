from django.db import models
import uuid
import os

"""
Generate unique name for each image in the folder posts
Source: https://stackoverflow.com/a/2677474/9655579
"""
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('posts', filename)

#Source: Model field reference https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.DateTimeField
class Genre(models.Model):

    #Text that will be shown in Django Admin fields for this model
    SHOW = 'YES'
    NOTSHOW = 'NO'
    SHOW_MENU_LIST_CHOICES = [
        (SHOW, 'Show in menu list'),
        (NOTSHOW, 'Not show in menu list'),
    ]

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    #Add data with text to the field
    show_menu_list = models.CharField(
        max_length=3,
        choices=SHOW_MENU_LIST_CHOICES,
        default=NOTSHOW,
    )
    image_genre = models.ImageField(upload_to=get_file_path, null=True, blank=True)

    def __str__(self):
        return self.name