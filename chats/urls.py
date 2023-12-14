from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('<int:own_id>,<int:foreign_id>/', views.create_chat, name='create_chat')
]