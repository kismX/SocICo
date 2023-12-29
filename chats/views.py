from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import Room, Message

@login_required
def rooms(request):
    profiles = get_user_model().objects.all()
    rooms = Room.objects.all()
    user_dict = dict()
    username_list = []

    for room in rooms:
        split_slug = room.slug.split('_')
        split_slug = [int(i) for i in split_slug]

        for i in split_slug:
            if i != request.user.id:
                for profile in profiles:
                    if i == profile.id:
                        name = profile.username
                username_list.append(name)

        if request.user.id in split_slug:
            user_dict[room.slug] = username_list

        username_list = []
    
    #print(user_dict)
    return render(request, 'chats/rooms.html', {'user_dict': user_dict})
        

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)

    return render(request, 'chats/room.html', {'room': room, 'messages': messages})

@login_required
def create_chat(request, own_id, foreign_id):
    first_id = str(own_id)
    second_id = str(foreign_id)

    slug1 = first_id + '_' + second_id
    slug2 = second_id + '_' + first_id

    if Room.objects.filter(slug=slug1):
        print('Room already exists')
        return redirect('rooms')
    elif Room.objects.filter(slug=slug2):
        print('Room already exists')
        return redirect('rooms')
    else:
        Room.objects.create(name=first_id+'_'+second_id, slug=first_id+'_'+second_id)
        return redirect('rooms')