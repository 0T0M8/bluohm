from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            from django.contrib import messages
            messages.error(request, "Passwords do not match")
            return redirect("/accounts/register/")

        user = User.objects.create_user(username=username, password=password)

        # Assign role
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save()

        return redirect("/accounts/login/")

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("marketplace")  # go home after login
        else:
            from django.contrib import messages
            messages.error(request, "Invalid username or password")
            return redirect("/accounts/login/")

    return render(request, "accounts/login.html")

@login_required
def dashboard_view(request):
    role = request.user.profile.role

    if role == "landlord":
        return render(request, "accounts/landlord_dashboard.html")

    else:
        return render(request, "accounts/tenant_dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
