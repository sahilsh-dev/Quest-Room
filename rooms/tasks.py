from celery import shared_task
from .models import QuestRoom, RoomCode
from django.utils import timezone


def remove_expired_items():
    QuestRoom.objects.filter(expires_at__lt=timezone.now()).delete()
    RoomCode.objects.filter(expires_at__lt=timezone.now()).delete()
