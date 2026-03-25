#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.landlord = request.user
            prop.save()
            return redirect('marketplace')
    else:
        form = PropertyForm()
    return render(request, 'properties/add_property.html', {'form': form})

@login_required
def marketplace(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'properties/marketplace.html', {'properties': properties})

def property_detail(request, id):
    property = get_object_or_404(Property, id=id)
    return render(request, 'properties/detail.html', {'property': property})
