# messaging/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Conversation, Message, ConversationReadState
from properties.models import Property


# ================================
# START CONVERSATION
# ================================
@login_required
def start_conversation(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    landlord = property_obj.owner
    user = request.user

    # Prevent self-chat
    if landlord == user:
        return redirect("properties:property_detail", property_id)

    # Check existing conversation
    conversation = Conversation.objects.filter(
        property=property_obj,
        participants=user
    ).filter(participants=landlord).first()

    if not conversation:
        conversation = Conversation.objects.create(property=property_obj)
        conversation.participants.add(user, landlord)

    return redirect("messaging:chat", conversation.id)


# ================================
# CHAT VIEW
# ================================
@login_required
def chat(request, conversation_id):

    conversation = Conversation.objects.filter(
        id=conversation_id,
        participants=request.user
    ).first()

    if not conversation:
        return redirect("messaging:inbox")

    # ✅ MARK AS READ
    read_state, _ = ConversationReadState.objects.get_or_create(
        user=request.user,
        conversation=conversation
    )
    read_state.last_read_at = timezone.now()
    read_state.save()

    # ✅ SEND MESSAGE (AJAX SAFE)
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            msg = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

            return JsonResponse({
                "status": "sent",
                "message_id": msg.id
            })

    messages = conversation.messages.order_by("created_at")

    return render(request, "messaging/chat.html", {
        "conversation": conversation,
        "messages": messages
    })


# ================================
# INBOX
# ================================
@login_required
def inbox(request):

    user = request.user

    conversations = Conversation.objects.filter(
        participants=user
    ).distinct()

    convo_data = []

    for convo in conversations:

        last_message = convo.messages.order_by("-created_at").first()

        read_state = ConversationReadState.objects.filter(
            user=user,
            conversation=convo
        ).first()

        if read_state and read_state.last_read_at:
            unread_count = convo.messages.filter(
                created_at__gt=read_state.last_read_at
            ).exclude(sender=user).count()
        else:
            unread_count = convo.messages.exclude(sender=user).count()

        convo.last_message = last_message
        convo.unread_count = unread_count

        convo_data.append(convo)

    return render(request, "messaging/inbox.html", {
        "conversations": convo_data
    })


# ================================
# FETCH MESSAGES (REAL-TIME)
# ================================
@login_required
def fetch_messages(request, conversation_id):

    conversation = Conversation.objects.filter(
        id=conversation_id,
        participants=request.user
    ).first()

    if not conversation:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    messages = conversation.messages.order_by("created_at")

    data = []
    last_id = 0

    for msg in messages:
        data.append({
            "id": msg.id,
            "content": msg.content,
            "is_me": msg.sender == request.user
        })
        last_id = msg.id

    return JsonResponse({
        "messages": data,
        "last_id": last_id
    })
