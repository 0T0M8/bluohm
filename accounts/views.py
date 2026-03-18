#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def register_view(request):
    return HttpResponse("Register page working!")