from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import Friendship
from accounts.models import Profile

def user_filter(request):
    current_user = request.user
    # friend_list = Friendship.objects.filter(Q(from_user=current_user, status='accepted') | Q(to_user=current_user, status='accepted'))
    users = get_user_model().objects.exclude(pk=request.user.pk)

    interests = request.GET.get('interests', '').lower()
    search_type = request.GET.get('search_type', 'contains')


    if interests:
        if search_type == 'contains':
            users = users.filter(profile__interests__icontains=interests)
        else:
            users = users.filter(profile__interests__iexact=interests)
    
    context = {'users': users, 'interests': interests}
    return render(request, 'user_filter.html', context)


