
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class SecurityConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, securityselector):
        task = PeriodicTask.objects.filter(name = "every-10-seconds")
        if len(task) > 0: # if > 0 means a task exists already so rather than creating a new one, the new arguements will be added.
            print("working")  # testing if task.first() works
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in securityselector:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args]) # Dump data into celery beats arguements.
            task.save()
        else: # Create task again.
            schedule, created = IntervalSchedule.objects.get_or_create(every=2, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds', task="main_app.tasks.update_security", args=json.dumps([securityselector]))
            # After task is added to periodic task table, celery will schedule it.

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'security_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Parse query_string
        query_params = parse_qs(self.scope["query_string"].decode())

        print(query_params)
        securityselector = query_params['securityselector']

        # Add to celery beat
        await self.addToCeleryBeat(securityselector)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': message
            }
        )

    # Receive message from room group
    async def send_security_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))