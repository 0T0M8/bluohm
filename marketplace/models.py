from django.db import models
from django.contrib.auth.models import User


LISTING_TYPE = (
    ('rent', 'Rent'),
    ('sale', 'Sale'),
)

PROPERTY_CATEGORY = (
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('townhouse', 'Townhouse'),
    ('land', 'Land'),
    ('commercial', 'Commercial'),
    ('student', 'Student Accommodation'),
    ('shortstay', 'Short Stay'),
)


class Property(models.Model):

    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    location = models.CharField(max_length=255)

    bedrooms = models.IntegerField()

    bathrooms = models.IntegerField()

    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPE,
        default='rent'
    )

    property_category = models.CharField(
        max_length=20,
        choices=PROPERTY_CATEGORY,
        default='house'
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titlefrom django.db import models

