from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import SchoolSerializers, SchoolDetailSerializers
from .models import School

# Create your views here.

class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializers

class SchoolDetailAPIView(RetrieveAPIView):

    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializers