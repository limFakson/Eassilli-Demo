from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    field = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="profile", null=False, on_delete=models.CASCADE
    )
    image = models.URLField(
        null=False, default="void/app/static/130-removebg-preview.png"
    )
    uid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False, null=False
    )

    def __str__(self):
        return self.user
