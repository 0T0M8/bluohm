# properties/urls.py
from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path("add/", views.add_property, name="add_property"),
    path("dashboard/", views.landlord_dashboard, name="landlord_dashboard"),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:property_id>/delete/', views.delete_property, name='delete_property'),
    path('favorite/<int:property_id>/', views.toggle_favorite, name='toggle_favorite'),
]
