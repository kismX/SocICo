from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Profile




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
    