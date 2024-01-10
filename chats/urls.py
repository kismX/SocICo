from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('create_group_chat/', views.create_group_chat, name='group_chat'),
    path('<slug:slug>/', views.room, name='room'),
    path('<int:own_id>/<int:foreign_id>/', views.create_private_chat, name='create_chat'),
]