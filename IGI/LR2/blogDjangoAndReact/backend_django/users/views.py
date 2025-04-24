from django.shortcuts import render
from django.http.response import JsonResponse
from django.contrib.auth.models import User

from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterUserSerializer,
    UpdateUserSerializer,
    ProfileImageSerializer
)
from .models import UserProfileImage

from rest_framework import status, generics, permissions

from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):

        user = User.objects.create(
            username=request.data.get('username'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            email=request.data.get('email'),
        )

        user.set_password(request.data.get('password'))
        user.save()

        user_profile_image = UserProfileImage.objects.create(
            user=user,
            profile_image=request.data.get('profile_image')
        )

        user_profile_image.save()

        serializer_class = self.serializer_class(user)
        return JsonResponse(serializer_class.data, safe=False, status=status.HTTP_200_OK)


class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # instance.username = request.data.get("username")
        instance.first_name = request.data.get("first_name")
        instance.last_name = request.data.get("last_name")
        instance.email = request.data.get("email")
        # instance.set_password(request.data.get('password'))
        instance.save()

        serializer = self.get_serializer(instance)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html#customizing-token-claims
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Generic class-based views for retrieving profile images list requests
class ProfileImagesListView(generics.ListAPIView):
    serializer_class = ProfileImageSerializer
    queryset = UserProfileImage.objects.all()