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
        print('Can Send Messages ->', has_perm_send_message)
        if not self.user.is_authenticated or not self.room or not has_perm_send_message:
            self.close()
            return
        
        self.room_group_name = self.room_id
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
        print(message)

        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        new_message = Message(room_id=self.room_id, user_id=self.user.id, content=message)
        new_message.save()
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
