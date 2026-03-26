# properties/urls.py
from django.urls import path
from .views import MarketplaceView, PropertyDetailView, AddPropertyView

app_name = 'properties'

urlpatterns = [
    path('', MarketplaceView.as_view(), name='marketplace'),
    path('add/', AddPropertyView.as_view(), name='add_property'),
    path('<int:id>/', PropertyDetailView.as_view(), name='property_detail'),
]
