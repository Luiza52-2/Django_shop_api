from django.db import models
from django.contrib.auth.models import User
import random


def generate_code():
    return str(random.randint(100000, 999999))


class UserConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6, default=generate_code)

    def __str__(self):
        return f'{self.user.username} — {self.code}'
