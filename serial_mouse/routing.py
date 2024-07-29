from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/serial/', consumers.SerialConsumer.as_asgi()),
]