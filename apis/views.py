from django.shortcuts import render
from rest_framework import generics
from accounts.models import Profile
from .serializer import ProfileSerializer

class ProfileData(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    