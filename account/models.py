from django.db import models
import uuid
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    field = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)

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


class ChatSystem(models.Model):
    chat_uid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    chat_type = models.CharField(max_length=50)
    user = models.ForeignKey(
        CustomUser, related_name="chat", null=False, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat_uid


class Message(models.Model):
    message_to = models.CharField(max_length=40)
    message_from = models.CharField(max_length=40)
    chat = models.ForeignKey(
        ChatSystem, on_delete=models.CASCADE, related_name="messages", null=False
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_to + "from" + self.message_from
