from django.urls import path
from .views import (
    UserProfileListView, UserProfileDetailView, SignUpView, 
    UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView,
    friend_requests, send_friend_request, accept_reject_friend
    )

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
    path("profiles/create", UserProfileCreateView.as_view(), name='profile_create'),
    path("profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile_edit'),
    path("profiles/<int:pk>/delete", UserProfileDeleteView.as_view(), name='profile_delete'),

    # 2023-11-22
    # path('friend_add/<int:friend_id>/', add_friends, name='add_friends'),
    path('friend_requests/', friend_requests,name='friend_requests'),
    #'friendship_ip' wird aus template geholt ( user klickt auf user, der id hat, die im template dann in friedship_id def. wird) 
    #'action' (wird hier definiert, um action zu machen ;) ) wird hier erstellt und an view 'accept_reject_friend' geschickt
    path('accept_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'accept'}, name='accept_friend'), 
    path('reject_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'reject'}, name='reject_friend'),

    path('send_friend_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'), # das to_user_id wird aus template geholt und an 'send_friend_request' gesendet

]