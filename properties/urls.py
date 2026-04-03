from django.urls import path
from . import views

urlpatterns = [
   path('', views.marketplace, name='marketplace'),
   path('add/', views.add_property, name='add_property'),
]
