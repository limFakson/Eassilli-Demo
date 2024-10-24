from django.db import models
from django.utils.timezone import now
from account.models import CustomUser

# Create your models here.


class Document(models.Model):
    file_url = models.URLField()
    user = models.ForeignKey(
        CustomUser, null=False, on_delete=models.CASCADE, related_name="document"
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user_id


class Lecturer(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="lecturer", null=False
    )
    email = models.EmailField(null=True)
    image = models.URLField(null=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class PastQues(models.Model):
    file_url = models.URLField()
    lecturer = models.ForeignKey(
        Lecturer, on_delete=models.CASCADE, related_name="past_ques", null=False
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)


class GenPastQues(models.Model):
    content = models.CharField(max_length=7000)
    lecturer = models.ForeignKey(
        Lecturer, on_delete=models.CASCADE, related_name="gen_pq", null=False
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)
