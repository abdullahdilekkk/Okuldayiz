from django.urls import path
from .views import SchoolListAPIView

urlpatterns = [
    path("list/", SchoolListAPIView.as_view(), name = "school-list"),
]


