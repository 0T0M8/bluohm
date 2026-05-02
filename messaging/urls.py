from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("start/<int:property_id>/", views.start_conversation, name="start"),
    path("chat/<int:conversation_id>/", views.chat_view, name="chat"),
    path("fetch/<int:conversation_id>/", views.fetch_messages, name="fetch"),
]

