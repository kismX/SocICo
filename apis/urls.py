from django.urls import path
from .views import ProfileData

urlpatterns = [
    path("profile_data/", ProfileData.as_view(), name="profile_data")
]