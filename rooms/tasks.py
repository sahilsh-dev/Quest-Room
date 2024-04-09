import requests
from django.utils import timezone
from celery import shared_task, current_app
from celery.schedules import crontab
from .models import User, QuestRoom, RoomCode, QuestRoomScore
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print('Setting up periodic tasks...')
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        remove_expired_items_task.s(),
    ) 
    sender.add_periodic_task(
        crontab(minute=50, hour='*'),
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
    url = "https://leetcode-stats-api.herokuapp.com/" + user.leetcode_username
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


def send_updated_scores_to_room(room_id, member_scores):
    channel_layer = get_channel_layer()
    player_scores = [
        (member.user.username, member.score) 
        for member in member_scores
    ]
    async_to_sync(channel_layer.group_send) (
        'chatroom_' + str(room_id), {
            'type': 'update_score_message',
            'message': player_scores
        }
    ) 


@shared_task
def update_questroom_score_task(room_id, send_updated=False):
    questroom_member_scores = QuestRoomScore.objects.filter(room_id=room_id).all()
    url = "https://leetcode-stats-api.herokuapp.com/"
    for member in questroom_member_scores:
        response = requests.get(url + member.user.leetcode_username)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                curr_problem_solved = data['totalSolved']
                member.score = curr_problem_solved - member.score_before_joining
                member.save()
                print(f"Updated score {member}")
        else:
            print(f"Failed to update score for {member.user.leetcode_username}")
    if send_updated:
        send_updated_scores_to_room(room_id, questroom_member_scores)
    

@shared_task
def update_all_questroom_scores_task():
    for questroom in QuestRoom.objects.all():
        update_questroom_score_task(questroom.id, send_updated=True)
    print(f"Updated scores for all rooms")
