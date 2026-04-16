from django.shortcuts import render, get_object_or_404
from properties.models import Property

def marketplace(request):
    properties = Property.objects.all().order_by('-created_at')

    return render(
        request,
        "marketplace/index.html",
        {"properties": properties}
    )


def property_detail(request, id):
    property = get_object_or_404(Property, id=id)

    return render(
        request,
        "marketplace/property_detail.html",
        {"property": property}
    )
