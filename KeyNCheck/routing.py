from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from Asistencia.consumers import consumidor

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", consumidor),
    ])
})
