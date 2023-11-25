from django.urls import path
from .views import (
    friend_requests, send_friend_request, accept_reject_friend
    )

# 2023-11-22
urlpatterns = [
# path('friend_add/<int:friend_id>/', add_friends, name='add_friends'),
    path('friend_requests/', friend_requests,name='friend_requests'),
    #'friendship_ip' wird aus template geholt ( user klickt auf user, der id hat, die im template dann in friedship_id def. wird) 
    #'action' (wird hier definiert, um action zu machen ;) ) wird hier erstellt und an view 'accept_reject_friend' geschickt
    path('accept_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'accept'}, name='accept_friend'), 
    path('reject_friend/<int:friendship_id>/', accept_reject_friend, {'action': 'reject'}, name='reject_friend'),

    path('send_friend_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'), # das to_user_id wird aus template geholt und an 'send_friend_request' gesendet
]