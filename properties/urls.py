from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_property, name='add_property'),
    path('', views.marketplace, name='marketplace'),
]
