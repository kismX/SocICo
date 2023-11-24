from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import Profile
from .forms import UpdateUserForm, UpdateProfileForm

# Password change:
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


class UserProfileListView(ListView): 
    model = Profile
    template_name = 'profile_list.html'

class UserProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile_detail')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile_edit')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    