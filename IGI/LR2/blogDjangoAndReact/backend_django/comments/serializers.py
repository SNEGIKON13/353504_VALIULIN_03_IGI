from rest_framework import serializers

from .models import Comment

#Serialize comments
class CommentSerializer(serializers.ModelSerializer):
    """
    Get username field from User model, one to many relation (author field)
    https://stackoverflow.com/a/46499968/9655579
    """
    username = serializers.CharField(read_only=True, source="author.username")

    class Meta:
        model = Comment
        fields = ['author', 'post','content','datetime', 'username']