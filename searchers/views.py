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
    users = get_user_model().objects.exclude(pk=request.user.pk)

    interests = request.GET.get('interests', '').lower()
    age = request.GET.get('age')
    gender = request.GET.get('gender')
    location = request.GET.get('location')
    last_online = request.GET.get('last_online')
    search_type = request.GET.get('search_type', 'contains')


    if interests:
        if search_type == 'contains':
            users = users.filter(profile__interests__icontains=interests)
        else:
            users = users.filter(profile__interests__iexact=interests)
        
    if age:
        users = users.filter(profile__age=age)
    
    if gender:
        users = users.filter(profile__gender=gender)

    if location:
        users = users.filter(profile__location=location)
    
    if last_online:
        last_online_cut = timezone.now() - timedelta(days=7)
        users = users.filter(profile__last_online__gte=last_online_cut)
    
    show_last_online = 'show_lasst_online' in request.GET
    
    context = {'users': users, 'interests': interests, 'age': age, 'gender': gender, 'location': location, 'last_online': last_online, 'show_last_online': show_last_online}
    return render(request, 'user_filter.html', context)


