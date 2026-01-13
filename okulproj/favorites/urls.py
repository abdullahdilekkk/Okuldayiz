from django.urls import path
from favorites.views import FavoriteListCreateAPIView, FavoriteDeleteAPIView
urlpatterns = [
    path("/api/favorites/list/", FavoriteListCreateAPIView.as_view(), name = "list-create"),
    path("delete/<int:pk>/", FavoriteDeleteAPIView.as_view(), name="delete")
]
