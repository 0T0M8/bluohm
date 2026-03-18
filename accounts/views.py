from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validation
        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect("/accounts/register/")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/accounts/register/")

        # Create user
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully!")

        return redirect("/accounts/login/")

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")  # go home after login
        else:
            from django.contrib import messages
            messages.error(request, "Invalid username or password")
            return redirect("/accounts/login/")

    return render(request, "accounts/login.html")

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
