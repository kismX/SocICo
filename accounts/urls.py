from django.urls import path
from .views import (
    UserProfileListView, UserProfileDetailView, SignUpView, profile, ChangePasswordView, 
    UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView,
    )

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
    path("profiles/create", UserProfileCreateView.as_view(), name='profile_create'),
    path("profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile_edit'),
    path("profiles/<int:pk>/delete", UserProfileDeleteView.as_view(), name='profile_delete'),

    path('profile-edit/', profile, name="profile_edit"),
]


