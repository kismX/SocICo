from django.urls import path
from .views import chatview

urlpatterns = [
    path('', chatview, name='chat-view')
]