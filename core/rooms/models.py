from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    admins = models.ManyToManyField(User)
    members = models.ManyToManyField(User, related_name='joined_rooms')
    expire_days = models.PositiveIntegerField(default=1)
    expires_at = models.DateTimeField()
    daily_required_points = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['name', 'created_by']]
        permissions = [
            # Default User Group Permissions
            ('can_send_message', 'Can send message in room'),

            # Admin User Group Permissions
            ('can_remove_user', 'Can remove user from room'),
            ('can_add_user', 'Can add user to room'),
            ('can_generate_roomcode', 'Can generate room code'),
        ]

    def __str__(self):
        return f'{self.created_by.username} - {self.name}'
        

class LatestMessages(models.Manager):
    def get_latest_messages(self, room_id, limit=30):
        return self.filter(room_id=room_id).order_by('-created_at')[:limit]


class Message(models.Model):
    room = models.ForeignKey(QuestRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    latest_messages = LatestMessages()
    
    def __str__(self):
        return f'{self.user.username} - {self.room.name} - {self.content[:20]}'


class RoomCode(models.Model):
    code = models.CharField(max_length=15, unique=True)
    room = models.ForeignKey(QuestRoom, on_delete=models.CASCADE, related_name='codes')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at + timezone.timedelta(days=self.room.expire_days) > timezone.now()
    
    def __str__(self):
        return f'{self.room.name} - {self.created_at}'
