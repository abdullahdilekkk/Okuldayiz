from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import LeadSerializer
from .models import Lead
from .permissions import IsLeadOwner
from rest_framework.permissions import IsAuthenticated, AllowAny
# Filtreleme için gerekli kütüphaneler:
from django_filters.rest_framework import DjangoFilterBackend # Net eşleşme (ID=5, called=False)
from rest_framework.filters import SearchFilter, OrderingFilter # Arama (name="Ali") ve Sıralama


from rest_framework.exceptions import ValidationError

class LeadCreateAPIView(CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [AllowAny]

    # perform_create: Django'nun "Tam kaydetme anı" metodudur.
    def perform_create(self, serializer):
        school_request_data = serializer.validated_data.get("school")
        current_signed_count = Lead.objects.filter(school=school_request_data, status = Lead.Status.SIGNED).count()

        if current_signed_count >= school_request_data.lead_limit:
            raise ValidationError({
                "error": "Bu okulun öğrenci kotası dolmuştur. Lütfen okul yönetimiyle iletişime geçin."
            })
        serializer.save()


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


    def perform_update(self, serializer):
        old_data = serializer.validated_data.get("status")
        new_data = serializer.instance.status

        if new_data == Lead.Status.SIGNED and old_data != Lead.Status.SIGNED:
            school = serializer.instance.school
            signed_count = Lead.objects.filter(school = school, status = Lead.Status.SIGNED).count()

            if signed_count >= school.lead_limit:
                 raise ValidationError({
                    "error": f"Kayıt kotanız ({school.lead_limit}) dolmuştur. Bu adayı 'Kayıt' durumuna alamazsınız."
                })
            
        serializer.save()


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q

class LeadDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_leads = Lead.objects.filter(school__owner = request.user)

        stats = my_leads.aggregate(
            total = Count("id"),
            new_leads_count = Count("id", filter = Q(status = Lead.Status.NEW)),
            contacted_leads_count = Count("id", filter = Q(status= Lead.Status.CONTACTED)),
            signed_leads_count = Count("id", filter = Q(status = Lead.Status.SIGNED)),
            negative_leads_count = Count("id", filter = Q(status = Lead.Status.NEGATIVE)),
            meeting_leads_count = Count("id", filter = Q(status = Lead.Status.MEETING))
        )

        return Response(stats)