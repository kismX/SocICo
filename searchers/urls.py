from django.urls import path
from .views import user_filter

urlpatterns = [
    path('user_filter/', user_filter, name='user_filter'),
]