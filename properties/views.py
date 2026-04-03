from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage
from .forms import PropertyForm
from django.contrib import messages

@login_required
def add_property(request):

    if request.method == 'POST':

        form = PropertyForm(request.POST)

        images = request.FILES.getlist('images')

        if form.is_valid():

            property = form.save(commit=False)
            property.landlord = request.user
            property.save()

            for image in images:
                PropertyImage.objects.create(
                    property=property,
                    image=image
                )

            messages.success(request, "Property added successfully!")

            return redirect('landlord_dashboard')

    else:
        form = PropertyForm()

    return render(request, 'properties/add_property.html', {
        'form': form
    })

def marketplace(request):

    properties = Property.objects.all().order_by('-created_at')

    return render(request, 'properties/marketplace.html', {
        'properties': properties
    })
