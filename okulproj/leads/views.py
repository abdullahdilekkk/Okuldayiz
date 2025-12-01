from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import LeadSerializer
from .models import Lead
# Create your views here.
class LeadCreateAPIView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    