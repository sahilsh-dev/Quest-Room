from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestRoom(models.Model):
    class RoomType(models.TextChoices):
        LEETCODE = 'LC', 'LeetCode'

    name = models.CharField(max_length=50)
    description = models.TextField()
    room_type = models.CharField(
        choices=RoomType.choices,
        default=RoomType.LEETCODE,
        max_length=2
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    members = models.ManyToManyField(User)
    expire_days = models.PositiveIntegerField(default=1)
    expires_at = models.DateTimeField()
    daily_required_points = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['name', 'created_by']]

    def __str__(self):
        return f'{self.created_by.username} - {self.name}'