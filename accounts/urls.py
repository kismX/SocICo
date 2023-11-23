from django.urls import path
from .views import UserProfileListView, UserProfileDetailView, SignUpView, friend_requests, send_friend_request, accept_reject_friend
from .views import UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profiles/', UserProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>', UserProfileDetailView.as_view(), name='profile_detail'),
    
    #2023-11-22
    path("profiles/create", UserProfileCreateView.as_view(), name='profile_create'),
    path("profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile_edit'),
    path("profiles/<int:pk>/delete", UserProfileDeleteView.as_view(), name='profile_delete'),

    # 2023-11-22
    # path('friend_add/<int:friend_id>/', add_friends, name='add_friends'),
    path('friend_requests/', friend_requests,name='friend_requests'),
    #'friendship_ip' wird aus dem template geholt (der user klickt auf einen user, der eine id hat, die im template dann friedship_id genannt wird) 
    # und 'action' (wird hier einfach defiiert und mitgeschickt an den view) wird hier genommen und an accept_reject_friend geschickt
    path('accept_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'accept'}, name='accept_friend'), 
    path('accept_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'reject'}, name='reject_friend'),

    path('send_friend_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'), # das to_user_id wird hier generiert und an send_friend_request gesendet


]