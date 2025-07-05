from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import UserSerializer
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model



# Authentication views
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer