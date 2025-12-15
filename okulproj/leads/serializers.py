from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = "__all__"
        # Kayıt işlemi yapacağımız için tüm alanları kabul etmeliyiz.
        # Frontend bize ne gönderirse (ad, soyad, okul id, plan id, opsiyon id'leri) alacağız.
    

    def validate(self, attrs):
        school = attrs.get("school")
        school_plan = attrs.get("school_plan")

        if school and school_plan:
            if school_plan.school != school:
                raise serializers.ValidationError({"school_plan": "Seçtiğiniz okul planı okula ait değil!"})

        return attrs

    def to_representation(self, instance):
        #Önce babasından (super) standart veriyi (ret) al.
        ret = super().to_representation(instance)

        if instance.school:
            ret["school_name"] = instance.school.name

        if instance.school_plan:
            ret["plan_title"] = instance.school_plan.title


        return ret
