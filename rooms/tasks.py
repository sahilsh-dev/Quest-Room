import requests
from django.utils import timezone
from celery import shared_task, current_app
from celery.schedules import crontab
from .models import User, QuestRoom, RoomCode, QuestRoomScore


@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print('Setting up periodic tasks...')
    sender.add_periodic_task(
        crontab(minute='*', hour='*'),
        remove_expired_items_task.s(),
    ) 
    sender.add_periodic_task(
        crontab(minute='*', hour='*'),
        update_all_questroom_scores_task.s(),
    )


@shared_task
def remove_expired_items_task():
    QuestRoom.objects.filter(expires_at__lt=timezone.now()).delete()
    print(f"Deleted expired rooms {timezone.now()}")
    RoomCode.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=1)).delete()
    print(f"Deleted expired room codes {timezone.now()}")


@shared_task
def set_initial_scores_task(room_id, user_id):
    user = User.objects.get(id=user_id)
    url = "https://leetcode-stats-api.herokuapp.com/" +  user.leetcode_username
    response = requests.get(url)    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            score = QuestRoomScore.objects.create(
                room_id=room_id, 
                user=user, 
                score_before_joining=data['totalSolved']
            )
            score.save()
            print(f"Saved initial score {score}")
            return True 
    return False

    
def update_questroom_score_task(room_id):
    questroom = QuestRoom.objects.get(id=room_id) 
    url = "https://leetcode-stats-api.herokuapp.com/"
    for user in questroom.members.all():
        response = requests.get(url + user.leetcode_username)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                questroom_score = QuestRoomScore.objects.get(room_id=room_id, user=user)
                curr_problem_solved = data['totalSolved']
                questroom_score.score = curr_problem_solved - questroom_score.score_before_joining
                print(f"Updated score {questroom_score}")
        else:
            print(f"Failed to update score for {user.leetcode_username}")
    print(f"Updated scores for room - {questroom}")

    
@shared_task
def update_all_questroom_scores_task():
    for questroom in QuestRoom.objects.all():
        update_questroom_score_task(questroom.id)
    print(f"Updated scores for all rooms")
