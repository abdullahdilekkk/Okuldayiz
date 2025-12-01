from django.shortcuts import render
import rest_framework
import rest_framework.filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import SchoolSerializers, SchoolDetailSerializers
from .models import School
import django_filters.rest_framework  #filtreleme için settings e de ekledim
import rest_framework.filters
# Create your views here.

class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializers

    # 1. DjangoFilter: Net eşleşme (Şehir=İzmir)
    # 2. SearchFilter: Kelime arama (Adı "Yıldız" olanlar)
    # 3. OrderingFilter: Sıralama (Fiyata göre artan/azalan)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter]
    
    # Hangi alanlara göre net filtreleme yapılacak?
    filterset_fields = ["city", "district", "school_type"]

    # Hangi alanlarda kelime aranacak?
    search_fields = ["name", "description", "address"]

    # Neye göre sıralama yapılabilecek?
    ordering_fields = ["id", "name"]


class SchoolDetailAPIView(RetrieveAPIView):

    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializers