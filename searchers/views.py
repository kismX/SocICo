from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import Friendship
from accounts.models import Profile

def user_filter(request):
    current_user = request.user
    # friend_list = Friendship.objects.filter(Q(from_user=current_user, status='accepted') | Q(to_user=current_user, status='accepted'))
    users = get_user_model().objects.exclude(pk=request.user.pk) # alle ohne request.user, wir wollen ja nicht, dass der selbst mit angezeigt wird, ne?

    # holt die interessen rein, die in der url im GET als value zum key interests angefordert werden
    # anschließend machen wir eine liste aller interessen, die wir am "," abspalten und mit strip alle leerzeichen entfernen
    # des weiteren holen wir values für age, gender usw
    interests = request.GET.get('interests', '')
    interest_list = [interest.strip().lower() for interest in interests.split(',')] if interests else []
    age = request.GET.get('age')
    gender = request.GET.get('gender')
    location = request.GET.get('location', '')
    last_online = request.GET.get('last_online')


    # user wählt contains oder exact, dann gehen wir liste der interessen durhc und wenn enthalten, wird ausgegeben
    # auf dauer kann datenmenge komplex sein.. dann evtl Q-abfrage implementieren
    if interests:
        for interest in interest_list:
                users = users.filter(profile__interests__icontains=interest)

    if age:
        users = users.filter(profile__age=age)
    
    if gender:
        users = users.filter(profile__gender=gender)
    
    if location:
        location = location.lower()
        users = users.filter(profile__location__icontains=location)

    if last_online:
        last_online_cut = timezone.now() - timedelta(days=7)
        users = users.filter(profile__last_online=last_online_cut)
    


    context = {'users': users, 'interests': interests, 'age': age, 'gender': gender, 'location': location, 'last_online': last_online, 'interest_list': interest_list}
    return render(request, 'user_filter.html', context)


