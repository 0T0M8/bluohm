#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
