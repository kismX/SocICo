from django.urls import path
from .views import chatview, chat_detail

urlpatterns = [
    path('', chatview, name='chat-view'),
    path('<slug:slug>/', chat_detail, name='room')     # <slug:slug> zuerst der erwartete datentyp und dann der name der auch in views.py in die function reingeht
]