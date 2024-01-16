from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from accounts.models import Friendship
from .models import Room, Message
from psycopg2 import errors


@login_required
def rooms(request):
    rooms = Room.objects.all()
    profiles = get_user_model().objects.all()
    private_dict = dict()
    group_dict = dict()
    username_list = []

    # Liste mit allen Namen der User in einem Chat erstellen:
    for room in rooms:
        for id in room.user_list:
            if id != request.user.id:
                profile = profiles.get(id=id)
                username_list.append(profile.username)

        # Wenn der eingeloggte User sich in dieser Liste befindet gib sie aus
        if request.user.id in room.user_list:
            if len(room.user_list) < 3:
                private_dict[room.slug] = username_list
            else:
                group_dict[room.slug] = room.name

        username_list = []

    context = {
        'private_dict': private_dict,
        'group_dict': group_dict
    }
    
    #print(user_dict)
    return render(request, 'chats/rooms.html', context)
        

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    profiles = get_user_model().objects.all()
    username_list = []

    for id in room.user_list:
        if id != request.user.id:
            profile = profiles.get(id=id)
            username_list.append(profile.username)

    return render(request, 'chats/room.html', {'room': room, 'messages': messages, 'username_list': username_list})


@login_required
def create_private_chat(request, own_id, foreign_id):

    rooms = Room.objects.all()
    id_list = [own_id, foreign_id]
    id_list.sort()
    str_ids = [str(num) for num in id_list]

    if rooms:
        for room in rooms:
            sorted_room_list = sorted(room.user_list)
            if sorted_room_list == id_list:
                print('Room already exists')
            else:
                try:
                    Room.objects.create(name='_'.join(str_ids), slug='_'.join(str_ids), user_list=[own_id, foreign_id])
                except (errors.UniqueViolation, IntegrityError):
                    print("Raum existiert schon")

    else:
        Room.objects.create(name='_'.join(str_ids), slug='_'.join(str_ids), user_list=[own_id, foreign_id])
    return redirect('rooms')


@login_required
def create_group_chat(request):
    user = request.user.id
    profiles = get_user_model().objects.exclude(pk=request.user.pk)
    friends = Friendship.objects.filter(from_user=user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=user, accepted_at__isnull=False)
    friends_list = []

    # Liste der eigenen Freunde
    for friend in friends:
        if friend.to_user_id == user:
            friends_list.append(friend.from_user)
        else:
            friends_list.append(friend.to_user)
    
    input_list = request.POST.getlist("input_all_users")
    input_name = request.POST.get("room_name")
    rooms = Room.objects.all()
    id_list = [user]

    # Wenn der Input nicht None ist erstelle einen Raum:
    if input_list != []:
        for item in input_list:
            item = int(item)
            if item not in id_list:
                id_list.append(item)

        sorted_id_list = sorted(id_list)
        sorted_id_list_strings = [str(id) for id in sorted_id_list]

        for room in rooms:
            sorted_room_list = sorted(room.user_list)
            print(sorted_room_list)

            if sorted_room_list == sorted_id_list:
                print('Room already exists')
            else:
                try:
                    Room.objects.create(name=input_name, slug='_'.join(sorted_id_list_strings), user_list=id_list)
                except (errors.UniqueViolation, IntegrityError):
                    print('Room already exists')
        #print('redirect')
        return redirect('rooms')

    context = {
        'profiles': profiles,
        'friends': friends_list,
    }    

    return render(request, 'chats/create_room.html', context)