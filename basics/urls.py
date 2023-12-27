from django.urls import path
from .views import home, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home, name='home'),
]

