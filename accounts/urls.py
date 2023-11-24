from django.urls import path
from .views import UserProfileListView, UserProfileDetailView, SignUpView, profile, ChangePasswordView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile-edit/', profile, name="profile_edit"),
] 

