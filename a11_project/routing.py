from django.urls import re_path
from .import consumer
#routing
#the routing.py file was created for the live chat feature

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
]