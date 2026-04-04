# properties/urls.py
from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path("add/", views.add_property, name="add_property"),
    path("dashboard/", views.landlord_dashboard, name="landlord_dashboard"),
]
