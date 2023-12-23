from django.urls import path
from .views import create_post, newsfeed, create_event

urlpatterns = [
    path('create_post/', create_post, name='create_post'),
    path('newsfeed/', newsfeed, name='newsfeed'),
    path('create_event/', create_event, name='create_event'),

]