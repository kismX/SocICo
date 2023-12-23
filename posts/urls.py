from django.urls import path
from .views import create_post, newsfeed, create_event, edit_post, delete_post

urlpatterns = [
    path('create_post/', create_post, name='create_post'),
    path('post_edit/<int:post_id>/', edit_post, name='edit_post'),
    path('post_delete/<int:post_id>/', delete_post, name='delete_post'),
    path('newsfeed/', newsfeed, name='newsfeed'),
    path('create_event/', create_event, name='create_event'),

]