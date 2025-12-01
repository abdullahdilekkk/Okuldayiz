from attr import field
from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"
        # Kayıt işlemi yapacağımız için tüm alanları kabul etmeliyiz.
        # Frontend bize ne gönderirse (ad, soyad, okul id, plan id, opsiyon id'leri) alacağız.