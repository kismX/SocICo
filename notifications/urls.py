from django.urls import path
from .views import mark_as_read, get_unsent_notifications

urlpatterns = [
    path('mark-as-read/', mark_as_read, name='mark-as-read'),
    path('unsent_notifications/', get_unsent_notifications, name='unsent_notifications'),
    
]