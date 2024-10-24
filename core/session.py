import os
import django
from django.conf import settings
from pydantic import BaseModel

# Django settings environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

# Initialise django
django.setup()


class UserModel(BaseModel):
    identifier: str
    password: str


class RegisterUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    userName: str
    isStudent: bool
    field: str
    password: str


class Speack(BaseModel):
    text: str
