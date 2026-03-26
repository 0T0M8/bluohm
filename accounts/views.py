# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile


@transaction.atomic
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:register")

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Create or get profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        messages.success(request, "Account created! Please login.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("properties:marketplace")  # go home after login
        else:
            messages.error(request, "Invalid username or password")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


@login_required
def dashboard_view(request):
    try:
        role = request.user.profile.role
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Contact admin.")
        return redirect("accounts:login")

    if role == "landlord":
        return render(request, "accounts/landlord_dashboard.html")
    else:
        return render(request, "accounts/tenant_dashboard.html")


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")
