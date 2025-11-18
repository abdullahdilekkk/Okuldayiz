from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import SchoolSerializers
from .models import School

# Create your views here.

class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializers

