from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api/schools/", include("schools.urls")),
    path("api/leads/", include("leads.urls"))
]
