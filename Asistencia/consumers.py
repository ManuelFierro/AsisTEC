from channels.generic.websocket import AsyncJsonWebsocketConsumer


class consumidor(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("msg", self.channel_name)
        print(f"Se agrego el canal {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("msg", self.channel_name)
        print(f"Se removio el canal {self.channel_name}")

    async def user_msg(self, event):
        await self.send_json(event)
        print(f"Se enviaron datos {event} a {self.channel_name}")