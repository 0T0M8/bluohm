#from django.contrib import admin

# Register your models here.
from django.urls import path
from .views import register_view

urlpatterns = [
    path('register/', register_view),
]