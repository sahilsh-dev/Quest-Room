from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    leetcode_username = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.username}'