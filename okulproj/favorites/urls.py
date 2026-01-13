from django.urls import path
from .views import FavoriteListCreateAPIView, FavoriteDeleteAPIView

urlpatterns = [

    path("list/", FavoriteListCreateAPIView.as_view(), name="list-create"),

    path("delete/<int:pk>/", FavoriteDeleteAPIView.as_view(), name="delete"),
]
