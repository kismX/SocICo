from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from posts.models import Post
from accounts.forms import CustomUserCreationForm
from .utils import get_domain
from django.contrib.auth import login
from django.shortcuts import redirect

#password change
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse_lazy('profile_edit'))


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Successfully Changed Your Password'
    success_url = reverse_lazy('profile_detail')


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # wenn link füge object das attribut .domain mit der url hinzu
    for post in posts:
        if post.link:
            post.domain = get_domain(post.link)
            
    return render(request, 'home.html', {'posts': posts})

