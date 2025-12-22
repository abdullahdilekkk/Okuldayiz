from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import LeadSerializer
from .models import Lead
from .permissions import IsLeadOwner
from rest_framework.permissions import IsAuthenticated, AllowAny
# Filtreleme için gerekli kütüphaneler:
from django_filters.rest_framework import DjangoFilterBackend # Net eşleşme (ID=5, called=False)
from rest_framework.filters import SearchFilter, OrderingFilter # Arama (name="Ali") ve Sıralama



class LeadCreateAPIView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [AllowAny]
    

class LeadListAPIView(ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'school']
    search_fields = ['name', 'surname']      # Nerede kelime aranacak?
    ordering_fields = ['time', 'name']

    def get_queryset(self):
        return Lead.objects.filter(school__owner = self.request.user)


class LeadDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, IsLeadOwner]

    def get_queryset(self):
        return Lead.objects.filter(school__owner = self.request.user)
    
    