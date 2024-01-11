from django.urls import path
from .views import get_notifications,  mark_as_read, get_unsent_notifications

urlpatterns = [
    path('notifications/', get_notifications, name='notifications'), # ohne websockets lösung

    path('mark-as-read/', mark_as_read, name='mark-as-read'),
    path('unsent_notifications/', get_unsent_notifications, name='unsent_notifications'),
    
]