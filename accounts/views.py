from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from .models import Profile
from django.urls import reverse_lazy




class UserProfileListView(ListView): 
    model = Profile
    template_name = 'profile_list.html'


class UserProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"
