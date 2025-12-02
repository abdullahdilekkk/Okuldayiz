from django.urls import path
from .views import LeadCreateAPIView,LeadListAPIView
urlpatterns = [
    path("create/", LeadCreateAPIView.as_view(), name="lead-create"),
    path("list/", LeadListAPIView.as_view(), name = "lead-list")
]
