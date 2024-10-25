from django.urls import path
from .views import views

urlpatterns = [
    path("", views.home),
    path("register", views.registration),
    path("login", views.login),
]
