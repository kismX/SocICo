from django.shortcuts import render

# Create your views here.
def chatview(request):
    return render(request, "base.html")