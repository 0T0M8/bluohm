# bluohm/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts.views import dashboard_view
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("🏠 Home page — you are logged in!")

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # ✅ simple include
    path("dashboard/", dashboard_view),
    path("properties/", include("properties.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
