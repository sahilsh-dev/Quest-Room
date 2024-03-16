import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #TODO: Use slugs in the URL
        self.room_group_name = self.scope['url_route']['kwargs']['room_id']
        self.current_user = self.scope['user']
        
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        print('User Connected:', self.current_user)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        new_message = Message(room_id=self.room_group_name, user_id=self.current_user.id, content=message)
        new_message.save()
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))