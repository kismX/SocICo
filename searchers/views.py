from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


def user_filter(request):
    # holen uns erstmal alle user, die wir später dann filtern je nach kategorie
    users = get_user_model().objects.exclude(pk=request.user.pk) # alle ohne request.user, wir wollen ja nicht, dass der selbst mit angezeigt wird, ne?

    # holt die interessen rein, die in der url im GET als value zum key interests angefordert werden
    # anschließend machen wir eine liste aller interessen, die wir am "," abspalten und mit strip alle leerzeichen entfernen
    # des weiteren holen wir values für age, gender usw
    interests = request.GET.get('interests', '')
    interest_list = [interest.strip().lower() for interest in interests.split(',')] if interests else []
    
    age = request.GET.get('age')
    min_age = request.GET.get('min_age') 
    max_age = request.GET.get('max_age')
    
    gender = request.GET.get('gender')
    location = request.GET.get('location', '')
    last_online = request.GET.get('last_online')
    last_online_cut = request.GET.get('last_online_cut', '')


    # user wählt contains oder exact, dann gehen wir liste der interessen durhc und wenn enthalten, wird ausgegeben
    # auf dauer kann datenmenge komplex sein.. dann evtl Q-abfrage implementieren
    if interests:
        for interest in interest_list:
                users = users.filter(profile__interests__icontains=interest) #speichern nur die leute in 'users' ab, die passende interessen haben

    if age:
        users = users.filter(profile__age=age)
    
    if min_age:
         users = users.filter(profile__age__gte=min_age)  #gte = g und gleich dem wert

    if max_age:
         users = users.filter(profile__age__lte=max_age)  #lte = kleiner und gleich dem wert

    if gender:
        users = users.filter(profile__gender=gender)
    
    if location:
        location = location.lower()
        users = users.filter(profile__location__icontains=location)

    if last_online_cut:
        days_num = int(last_online_cut)
        last_online_delta = timezone.now() - timedelta(days=days_num) #errechne mir einen zeitpunkt: aktuell minus der tage, die der user eingegeben hat
        users = users.filter(profile__last_online__gte=last_online_delta) # alle user die ab dem zeitpunkt bis heut online waren werden aufgelistet
    

    context = {'users': users, 'interests': interests, 'interest_list': interest_list, 
               'age': age, 'min_age': min_age, 'max_age': max_age, 'gender': gender, 
               'location': location, 'last_online': last_online}
    
    return render(request, 'searchers/user_filter.html', context)


