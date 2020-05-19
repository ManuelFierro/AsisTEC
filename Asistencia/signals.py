from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(user_logged_in, sender=User)
def announce_new_user(sender, request, user , **kwargs):
    if request:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "msg", {"type": "user.msg",
                       "event": "logeo",
                       "username": user.username,
                       "firstname": user.first_name,
                       "lastname": user.last_name,},)
                       
