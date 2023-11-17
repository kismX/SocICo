from django.urls import path
from .views import UserProfileListView, UserProfileDetailView

urlpatterns = [
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
]