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
    profiles = get_user_model().objects.all()
    rooms = Room.objects.all()
    user_dict = dict()
    username_list = []

    # Liste mit allen Namen der User in einem Chat erstellen:
    for room in rooms:
        for id in room.user_list:
            if id != request.user.id:
                profile = profiles.get(id=id)
                username_list.append(profile.username)

        # Wenn der eingeloggte User sich in dieser Liste befindet gib sie aus
        if request.user.id in room.user_list:
            user_dict[room.slug] = username_list

        username_list = []
    
    #print(user_dict)
    return render(request, 'chats/rooms.html', {'user_dict': user_dict})
        

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    profiles = get_user_model().objects.all()
    user_dict = dict()
    username_list = []

    for id in room.user_list:
        if id != request.user.id:
            profile = profiles.get(id=id)
            username_list.append(profile.username)

        if request.user.id in room.user_list:
            user_dict[room.slug] = username_list

        username_list = []

    return render(request, 'chats/room.html', {'room': room, 'messages': messages, 'user_dict': user_dict})

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
    profiles = get_user_model().objects.all()
    user = request.user.id
    friends = Friendship.objects.filter(from_user=user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=user, accepted_at__isnull=False)
    input_list = request.GET.getlist("input_all_users")
    input_name = request.GET.get("room_name")
    id_list = [user]


    if input_list != []:
        for item in input_list:
            item = int(item)
            id_list.append(item)
        
        Room.objects.create(name=input_name, slug=str(user)+'_'+'_'.join(input_list), user_list=id_list)
        return redirect('rooms')

    context = {
        'profiles': profiles,
        'friends': friends,
    }    

    return render(request, 'chats/create_room.html', context)