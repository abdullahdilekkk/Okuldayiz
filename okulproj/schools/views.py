from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import SchoolSerializers, SchoolDetailSerializers
from .models import School
from django_filters.rest_framework import DjangoFilterBackend   #filtreleme için settings e de ekledim

# Create your views here.

class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializers

    filter_backends = [DjangoFilterBackend]
    filterset_set =["city", "district", "school_type"]

class SchoolDetailAPIView(RetrieveAPIView):

    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializers