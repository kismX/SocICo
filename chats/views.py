from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatRoom

@login_required
def chatview(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, "chats/chatroom.html", {'rooms': chatrooms})

@login_required
def chat_detail(request, slug):
    room = ChatRoom.objects.get(slug=slug)
    return render(request, "chats/room.html", {'room': room})