from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'^ws/conversation/(?P<conversation_id>\d+)/$', consumer.ChatConsumer.as_asgi()),
]
