from django.shortcuts import render
import rest_framework
import rest_framework.filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SchoolSerializers, SchoolDetailSerializers, SchoolUpdateSerializers
from .models import School
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly

class SchoolListAPIView(ListAPIView):

    serializer_class = SchoolSerializers
    permission_classes = [AllowAny]
    # 1. DjangoFilter: Net eşleşme (Şehir=İzmir)
    # 2. SearchFilter: Kelime arama (Adı "Yıldız" olanlar)
    # 3. OrderingFilter: Sıralama (Fiyata göre artan/azalan)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Hangi alanlara göre net filtreleme yapılacak?
    filterset_fields = ["city", "district", "school_type"]
    # Hangi alanlarda kelime aranacak?
    search_fields = ["name", "description", "address"]
    # Neye göre sıralama yapılabilecek?
    ordering_fields = ["id", "name"]

    def get_queryset(self):
        return School.objects.filter(
            is_active=True 
        ).select_related(
            'city',      # ForeignKey (Her okulun 1 şehri var)
            'district',  # ForeignKey (Her okulun 1 ilçesi var)
            'owner'      # ForeignKey (Her okulun 1 sahibi var)
        ).prefetch_related(
            'features'   # ManyToMany (Her okulun N tane özelliği olabilir)
        ).all()


class SchoolDetailAPIView(RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializers
    permission_classes = [AllowAny]

from rest_framework.exceptions import NotFound

class SchoolManagementAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return School.objects.get(owner=self.request.user)
        except School.DoesNotExist:
            raise NotFound("Size ait bir okul bulunamadı.")
        
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SchoolUpdateSerializers
        
        return SchoolDetailSerializers
    
    def perform_destroy(self, instance):
        if hasattr(instance, 'is_active'):
            instance.is_active = False
            instance.save()