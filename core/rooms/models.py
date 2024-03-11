from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestRoom(models.Model):
    class RoomType(models.TextChoices):
        LEETCODE = 'LC', 'LeetCode Quest'

    name = models.CharField(max_length=140, unique=True)
    description = models.TextField()
    room_type = models.CharField(
        choices=RoomType.choices,
        default=RoomType.LEETCODE,
        max_length=2
    )
    head = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='rooms')
    expire_days = models.PositiveIntegerField(default=1)
    expires_at = models.DateTimeField()
    daily_required_points = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{head.username}-{self.name}'