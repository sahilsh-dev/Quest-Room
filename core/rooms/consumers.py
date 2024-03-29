import json
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

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('User:', self.user.username, '->', message, '->', self.room_group_name)
        new_message = Message(room_id=self.room_id, user_id=self.user.id, content=message)
        new_message.save()
        print('New Message Saved: ', new_message)
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name, {
                'type': 'chat.message',
                'username': self.user.username,
                'content': new_message.content,
                'message_time': new_message.get_message_time(),
            }
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

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )
