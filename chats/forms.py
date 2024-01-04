from django import forms
from accounts.models import Friendship, Profile
from django.contrib.auth import get_user_model

class CreateChatForm(forms.Form):
    profiles = Profile.objects.all()
    user = get_user_model()
    profile = None
    get_friends = Friendship.objects.filter(from_user=profile, accepted_at__isnull=False) | Friendship.objects.filter(to_user=profile, accepted_at__isnull=False)

    for x in profiles:
        if x == user:
           profile = x

    CHOICES = ((1, "hallo"),
                (2, "banane"),
                (3, "apfel"))

    
    friend_list = get_friends.values_list()
    friends = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)