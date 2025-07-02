
from django.contrib.auth.models import User
from django.db import models
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username