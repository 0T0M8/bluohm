from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Property, PropertyImage

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

@login_required
def landlord_dashboard(request):

    properties = Property.objects.filter(owner=request.user)

    return render(request, "properties/landlord_dashboard.html", {
        "properties": properties
    })
