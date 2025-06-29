from channels.generic.websocket import AsyncWebsocketConsumer
import json

class IPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = f'task_{self.task_id}'
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    async def ip_result(self, event):
        await self.send(text_data=json.dumps({
            'task_id': event['task_id'],
            'ip': event['ip'],
            'result': event['result'],
        }))