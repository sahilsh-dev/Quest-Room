import json
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, QuestRoom

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        #TODO: Use slugs in the URL
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = QuestRoom.objects.get(id=self.room_id)

        has_perm_send_message = self.user.has_perm('rooms.can_send_message', self.room)
        if not self.user.is_authenticated or not self.room or not has_perm_send_message:
            self.close()
            return
        
        self.room_group_name = f'chatroom_{self.room_id}'
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected to room - ' + self.room_group_name 
        }))

        user_connected_time = timezone.now()
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name, {
                'type': 'user_connected_message',
                'content': f'{self.user.username} connected to the room',
                'message_time': user_connected_time.strftime('%H:%M'),
            }
        )
        user_connected_message = Message.objects.create (
            room_id=self.room_id,
            user=self.user,
            content=f'{self.user.username} connected to the room',
            message_type=Message.MessageType.USER_CONNECTED,
            created_at=user_connected_time
        )    
        user_connected_message.save()
            
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_time = timezone.now()
        print('User:', self.user.username, '->', message, '->', self.room_group_name)
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name, {
                'type': 'chat_message',
                'username': self.user.username,
                'content': message,
                'message_time': message_time.strftime('%H:%M'),
            }
        )
        chat_message = Message.objects.create (
            room_id=self.room_id, 
            user=self.user, 
            content=message, 
            message_type=Message.MessageType.CHAT,
            created_at=message_time
        )
        chat_message.save()

    def disconnect(self, error_code):
        message_time = timezone.now()
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name, {
                'type': 'user_left_message',
                'content': f'{self.user.username} left the room',
                'message_time': message_time.strftime('%H:%M'),
            }
        )
        user_left_message = Message.objects.create (
            room_id=self.room_id, 
            user=self.user, 
            content=f'{self.user.username} left the room', 
            message_type=Message.MessageType.USER_LEFT,
            created_at=message_time
        )
        user_left_message.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': {
                'username': event['username'],
                'content': event['content'],
                'message_time': event['message_time'],
            }
        }))

    def user_connected_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_connected',
            'message': {
                'content': event['content'],
                'message_time': event['message_time'],
            }
        }))

    def user_left_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_left',
            'message': {
                'content': event['content'],
                'message_time': event['message_time']
            }
        }))
