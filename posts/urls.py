from django.urls import path
from .views import (
        create_post, create_event, edit_post, delete_post, 
        post_detail, like_post, comment_edit, comment_delete
    )

urlpatterns = [
    path('create_post/', create_post, name='create_post'),
    path('post_edit/<int:post_id>/', edit_post, name='edit_post'),
    path('post_delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('comment/edit/<int:comment_id>/', comment_edit, name='comment_edit'),
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('post/like/<int:post_id>/', like_post, name='like_post'),
    path('create_event/', create_event, name='create_event'),

]