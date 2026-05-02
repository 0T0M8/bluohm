from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, PropertyImage, Favorite
from .forms import PropertyForm

@login_required
def add_property(request):

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        location = request.POST.get("location")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        property = Property.objects.create(
            owner=request.user,
            title=title,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            location=location,
            latitude=latitude,
            longitude=longitude,
        )

        for image in request.FILES.getlist("images"):
            PropertyImage.objects.create(
                property=property,
                image=image
            )

        return redirect("properties:landlord_dashboard")

    return render(request, "properties/add_property.html")

def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property)

        if form.is_valid():
            form.save()
            return redirect('properties:property_detail', property.id)

    else:
        form = PropertyForm(instance=property)

    return render(request, "properties/add_property.html", {
        "form": form
    })

def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    property.delete()

    return redirect('properties:landlord_dashboard')

@login_required
def landlord_dashboard(request):

    properties = Property.objects.filter(owner=request.user)

    return render(request, "properties/landlord_dashboard.html", {
        "properties": properties
    })

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    images = property.images.all()  # Assuming a related model for multiple images
    context = {
        'property': property,
        'images': images,
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def toggle_favorite(request, property_id):

    if request.method == "POST":
        property_obj = get_object_or_404(Property, id=property_id)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property_obj
        )

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')

    properties = [fav.property for fav in favorites]

    return render(request, "properties/favorites.html", {
        "properties": properties
    })
