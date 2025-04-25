from django.db import models
from posts.models import Post

from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='commentps')
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='commentus')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
