from django.urls import path
from .views import LeadCreateAPIView, LeadListAPIView, LeadDetailAPIView
urlpatterns = [
    path("create/", LeadCreateAPIView.as_view(), name = "lead-create"),
    path("list/", LeadListAPIView.as_view(), name = "lead-list"),
    path("detail/<int:pk>/", LeadDetailAPIView.as_view(), name = "lead-detail"),
]
