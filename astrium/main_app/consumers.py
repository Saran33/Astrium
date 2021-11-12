
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from main_app.models import SecurityProfile
import copy

class SecurityConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, securityselector):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        # if > 0 means a task exists already so rather than creating a new one, the new arguements will be added.
        if len(task) > 0:
            print("working")  # testing if task.first() works
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in securityselector:
                if x not in args:
                    args.append(x)
            # Dump data into celery beats arguements.
            task.args = json.dumps([args])
            task.save()
        else:  # Create task again.
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds',
                                               task="main_app.tasks.update_security", args=json.dumps([securityselector]))
            # After task is added to periodic task table, celery will schedule it.

    @sync_to_async
    def addToSecurityProfile(self, securityselector):
        user = self.scope["user"]
        for i in securityselector:
            security, created = SecurityProfile.objects.get_or_create(security=i)
            security.user.add(user)

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

        # Add user to securityprofile
        await self.addToSecurityProfile(securityselector)


        await self.accept()

    @sync_to_async
    def helper_func(self):
        user = self.scope["user"]
        securities = SecurityProfile.objects.filter(user__id = user.id) # __ because user is the foreign M-to-M key of the security
        task = PeriodicTask.objects.get(name = "every-10-seconds")
        args = json.loads(task.args)
        args = args[0]
        for i in securities:
            i.user.remove(user)
            if i.user.count() == 0:
                args.remove(i.security)
                i.delete()
        if args == None:
            args = []

        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args]) # Store to task args feed
            task.save()

    async def disconnect(self, close_code):
        await self.helper_func()

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

    @sync_to_async
    def selectUserSecurities(self):
        user = self.scope["user"]
        user_securities = user.securityprofile_set.values_list('security', flat=True) # Parse securities from db (Use set because M-to-M relationship). Only retrieve the ticker.
        return list(user_securities)


    # Receive message from room group
    async def send_security_update(self, event):
        message = event['message']
        message = copy.copy(message)

        user_securities = await self.selectUserSecurities()

        keys = message.keys()
        for key in list(keys):
            if key in user_securities:
                pass
            else:
                del message[key]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
