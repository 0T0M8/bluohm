from django.urls import re_path

from .consumers import ChatConsumer, InboxConsumer


websocket_urlpatterns = [

    # REAL-TIME CHAT
    re_path(
        r"ws/chat/(?P<conversation_id>\d+)/$",
        ChatConsumer.as_asgi()
    ),

    # REAL-TIME INBOX
    re_path(
        r"ws/inbox/$",
        InboxConsumer.as_asgi()
    ),

]
