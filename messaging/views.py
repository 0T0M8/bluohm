# messaging/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message
from properties.models import Property


@login_required
def start_conversation(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    landlord = property_obj.owner
    user = request.user

    # check existing conversation
    conversation = Conversation.objects.filter(
        property=property_obj,
        participants=user
    ).filter(participants=landlord).first()

    if not conversation:
        conversation = Conversation.objects.create(property=property_obj)
        conversation.participants.add(user, landlord)

    return redirect("messaging:chat", conversation.id)


@login_required
def chat_view(request, conversation_id):

    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

        return redirect("messaging:chat", conversation.id)

    messages = conversation.messages.all().order_by("-created_at")

    return render(request, "messaging/chat.html", {
        "conversation": conversation,
        "messages": messages
    })

@login_required
def fetch_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    messages = conversation.messages.all().order_by("-created_at")

    data = [
        {
            "sender": msg.sender.username,
            "content": msg.content,
            "is_me": msg.sender == request.user
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data})

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).order_by("-updated_at")

    inbox_data = []

    for convo in conversations:
        last_message = Message.objects.filter(
            conversation=convo
        ).order_by("-created_at").first()

        inbox_data.append({
            "conversation": convo,
            "last_message": last_message
        })

    return render(request, "messaging/inbox.html", {
        "inbox_data": inbox_data
    })

