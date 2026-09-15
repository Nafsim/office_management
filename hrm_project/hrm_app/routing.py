from django.urls import re_path

from .consumers import SupportChatConsumer


websocket_urlpatterns = [
    re_path(r'ws/support/chat/(?P<conversation_id>\d+)/$', SupportChatConsumer.as_asgi()),
]