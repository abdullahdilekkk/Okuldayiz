from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import LeadSerializer
from .models import Lead
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

# Filtreleme için gerekli kütüphaneler:
from django_filters.rest_framework import DjangoFilterBackend # Net eşleşme (ID=5, called=False)
from rest_framework.filters import SearchFilter, OrderingFilter # Arama (name="Ali") ve Sıralama

# Create your views here.
class LeadCreateAPIView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    

class LeadListAPIView(ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated, )

    

    def get_queryset(self):
        return Lead.objects.filter(school__owner = self.request.user)
    