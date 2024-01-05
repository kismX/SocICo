from django.urls import path
from .views import (
    UserProfileListView, UserProfileDetailView, 
    UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView,
    friend_requests, send_friend_request, accept_reject_friend, profile, 
    remove_friend, invisible_check,
    )

urlpatterns = [    
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
    path("profiles/create", UserProfileCreateView.as_view(), name='profile_create'),
    path("profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile_edit'),
    path("profiles/<int:pk>/delete", UserProfileDeleteView.as_view(), name='profile_delete'),
    path('profile-edit/', profile, name='profile_edit'),
    path('profile/invisible/', invisible_check, name='invisible_check'),

    path('friend_requests/', friend_requests,name='friend_requests'),

    path('accept_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'accept'}, name='accept_friend'), 
    path('reject_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'reject'}, name='reject_friend'),
    path('send_friend_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'), # das to_user_id wird aus template geholt und an 'send_friend_request' gesendet
    path('withdraw_friend_request/<int:profile_id>/', remove_friend, name='withdraw_friend_request'), 
    path('remove_friend/<int:profile_id>/', remove_friend, name='remove_friend'), 

]