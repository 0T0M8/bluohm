# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


@transaction.atomic
def register_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")
        role = request.POST.get("role")

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("accounts:register")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Update Profile
        profile = user.profile
        profile.role = role
        profile.phone = phone
        profile.save()

        # Send Welcome Email (Optional but nice)
        try:
            send_mail(
                "Welcome to Bluohm",
                f"Hi {username}, welcome to Bluohm!",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=True,
            )
        except:
            pass

        messages.success(request, "Account created successfully! Please login.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        try:
            user_obj = User.objects.get(email__iexact=email)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:
                login(request, user)

                role = getattr(
                    getattr(user, "profile", None),
                    "role",
                    "tenant"
                )

                if role == "landlord":
                    return redirect("properties:landlord_dashboard")

                elif role == "agent":
                    return redirect("properties:agent_dashboard")

                elif role == "tenant":
                    return redirect("marketplace:marketplace")

                else:
                    return redirect("marketplace:marketplace")

            else:
                messages.error(request, "Invalid email or password")

        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html")

@login_required
def dashboard_view(request):

    role = request.user.profile.role

    if role == "landlord":
        return render(request, "accounts/landlord_dashboard.html")

    elif role == "agent":
        return render(request, "accounts/agent_dashboard.html")

    else:
        return render(request, "accounts/tenant_dashboard.html")


@login_required
def logout_view(request):

    logout(request)
    # messages.info(request, "You have been logged out.")
    return redirect("accounts:login")
