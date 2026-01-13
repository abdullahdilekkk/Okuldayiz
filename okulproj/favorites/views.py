from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class FavoriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user = self.request.user)
    

class FavoriteDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user = self.request.user)