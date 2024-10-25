from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "backend/home.html")


def registration(request):
    return render(request, "auth/register.html")


def login(request):
    return render(request, "auth/login.html")
