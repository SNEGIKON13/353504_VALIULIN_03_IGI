from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfileImage
"""
Serializers to send or save data from models
"""

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        write_only_fields = ('password',)

    """
    Validaations for user registration and set secure password
    Source:
    https://stackoverflow.com/a/29867704/9655579
    """
    """
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()


        user_profile_image = UserProfileImage(
            user=user,
            profile_image=validated_data['profile_image']
        )

        user_profile_image.save()


        return user
        """


# Serialize Image profile nested array
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = ('__all__')


# Update profile data
class UpdateUserSerializer(serializers.ModelSerializer):
    # Set profile_image one to one relationship no nested object
    # source https://stackoverflow.com/a/31947249/9655579
    profile_image = serializers.ImageField(source='user_profile_image.profile_image')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'profile_image']
        write_only_fields = ('password',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizing JWT response from django-rest-framework-simplejwt
    https://stackoverflow.com/a/55859751/9655579
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        # data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

