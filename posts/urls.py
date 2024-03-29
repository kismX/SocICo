from django.urls import path
from .views import (
        create_post, create_event, edit_post, delete_post, 
        update_post_feed,
        post_detail, comment_edit, comment_delete,
        like_list_post, like_list_comment,
        like_post_ajax, like_comment_ajax
    )

urlpatterns = [
    path('create_post/<int:profile_id>/', create_post, name='create_post'),
    path('post_edit/<int:post_id>/', edit_post, name='edit_post'),
    path('post_delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('update_post_visibility/', update_post_feed, name='update_post_feed'),
    #path('update_all_post_feed/', update_all_posts_feed, name='update_all_posts_feed'),


    path('comment/edit/<int:comment_id>/', comment_edit, name='comment_edit'),
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    
    path('ajax/like_post/', like_post_ajax, name='like_post_ajax'),
    path('post/likelist/<int:post_id>/', like_list_post, name='likelist_post' ),
    path('ajax/like_comment/', like_comment_ajax, name='like_comment_ajax'),
    path('comment/likelist/<int:comment_id>/', like_list_comment, name='likelist_comment'),
    
    path('create_event/', create_event, name='create_event'),


]