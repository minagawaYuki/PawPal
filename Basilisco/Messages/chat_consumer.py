from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
    sender = self.scope['user'].username
    message = text_data.strip()

    chat_room = ChatRoom.objects.get(id=self.room_id)
    message = Message.objects.create(room=chat_room, sender=self.scope['user'], content=message)

    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'send_message',
            'message': f'{sender}: {message.content}'
        }
    )

    async def send_message(self, event):
        await self.send(text_data=event['message'])