from django.urls import path
from .views import SchoolListAPIView, SchoolDetailAPIView

urlpatterns = [
    path("list/", SchoolListAPIView.as_view(), name = "school-list"),
    path("list/<int:pk>/", SchoolDetailAPIView.as_view(), name = "school-detail"),
]


