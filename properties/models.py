from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    bedrooms = models.IntegerField(default=0)

    bathrooms = models.IntegerField(default=0)

    location = models.CharField(max_length=255)

    latitude = models.FloatField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to="properties/")
