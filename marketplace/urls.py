from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),
]
