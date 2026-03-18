
from django.urls import path
from .views import register_view, login_view, logout_view

def home(request):
    return HttpResponse("Hello from Termux Django!")

urlpatterns = [
    path('', home),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
]
