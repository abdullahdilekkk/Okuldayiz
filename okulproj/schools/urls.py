from django.urls import path
from .views import SchoolListAPIView, SchoolDetailAPIView, SchoolManagementAPIView

urlpatterns = [
    path("list/", SchoolListAPIView.as_view(), name = "school-list"),
    path("detail/<int:pk>/", SchoolDetailAPIView.as_view(), name = "school-detail"),
    path("manage/<int:pk>/", SchoolManagementAPIView.as_view(), name = "school-manage"),
]

