import requests
from celery import shared_task
from .models import User, QuestRoom, RoomCode, QuestRoomScore
from django.utils import timezone


@shared_task
def remove_expired_items():
    QuestRoom.objects.filter(expires_at__lt=timezone.now()).delete()
    RoomCode.objects.filter(expires_at__lt=timezone.now()).delete()


@shared_task
def set_initial_scores_task(room_id, user_id):
    user = User.objects.get(id=user_id)
    url = "https://leetcode-stats-api.herokuapp.com/" +  user.leetcode_username
    response = requests.get(url)    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            score = QuestRoomScore.objects.create(room_id=room_id, user=user, score_before_joining=data['totalSolved'])
            score.save()
            print(f"Saved initial score {score}")
            return True 
    return False
