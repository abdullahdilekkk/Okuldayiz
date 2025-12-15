from django.shortcuts import render
import rest_framework
import rest_framework.filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import SchoolSerializers, SchoolDetailSerializers
from .models import School
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly

class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
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


class SchoolDetailAPIView(RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializers
    permission_classes = [AllowAny]


class SchoolManagementAPIView(RetrieveUpdateAPIView):
    serializer_class = SchoolSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return School.objects.filter(owner = self.request.user)
