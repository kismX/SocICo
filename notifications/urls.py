from django.urls import path
from .views import mark_as_read

urlpatterns = [
    path('mark-as-read/', mark_as_read, name='mark-as-read'),

]