from django.urls import path
from .auth import authentication, profile

# from .api import
from . import views

urlpatterns = [
    path("auth/login", authentication.userLogin),
    path("auth/register", authentication.userregistration),
    path("auth/me", authentication.me),
    path("auth/profile", profile.profile_update),
]
