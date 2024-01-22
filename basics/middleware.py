from django.shortcuts import redirect
from django.urls import reverse

def is_profile_complete(user):
    return(
        user.profile.bio and
        user.profile.interests
    )

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.user.is_authenticated and
            not is_profile_complete(request.user) and
            request.path != reverse('profile_edit')
        ):
            return redirect(reverse('profile_edit'))
        
        return response