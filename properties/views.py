# properties/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Property
from .forms import PropertyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# -------------------------------
# Marketplace (List)
# -------------------------------
class MarketplaceView(View):
    def get(self, request):
        properties = Property.objects.all()
        return render(request, 'properties/marketplace.html', {'properties': properties})

# -------------------------------
# Property Detail
# -------------------------------
class PropertyDetailView(View):
    def get(self, request, id):
        property_obj = get_object_or_404(Property, id=id)
        return render(request, 'properties/detail.html', {'property': property_obj})

# -------------------------------
# Add Property (only landlords)
# -------------------------------
@method_decorator(login_required, name='dispatch')
class AddPropertyView(View):
    def get(self, request):
        if request.user.profile.role != 'landlord':
            return redirect('properties:marketplace')
        form = PropertyForm()
        return render(request, 'properties/add_property.html', {'form': form})

    def post(self, request):
        if request.user.profile.role != 'landlord':
            return redirect('properties:marketplace')
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.landlord = request.user
            property_obj.save()
            return redirect('properties:marketplace')
        return render(request, 'properties/add_property.html', {'form': form})
