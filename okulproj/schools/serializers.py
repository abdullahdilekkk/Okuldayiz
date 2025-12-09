from rest_framework import serializers
from .models import AdditionalFee, Language, School
from accounts.serializers import CitySerializers, DistrictSerializers




class SchoolSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only =True)
    name = serializers.CharField()
    slug = serializers.SlugField()
    school_type = serializers.CharField()
    address = serializers.CharField()

    city = CitySerializers(read_only=True)
    district = DistrictSerializers(read_only=True)

    city_id = serializers.IntegerField(write_only = True, required=False)
    district_id = serializers.IntegerField(write_only = True, required=False)


    def update(self, instance, validated_data):
        """
        instance: Veritabanındaki kayıtlı okul (Değişmeden önceki hali)
        validated_data: Frontend'den gelen yeni veriler (Değişecek hali)
        """

        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.school_type = validated_data.get("school_type", instance.school_type)
        instance.address = validated_data.get("address", instance.address)

        instance.city_id = validated_data.get("city_id", instance.city_id)
        instance.district_id = validated_data.get("district_id", instance.district_id)


        instance.save()
        return instance 
        



            










class LanguageSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()

class ServiceSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    icon = serializers.CharField()

class SchoolFeatureSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField()

class PlanOptionSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    plan_id = serializers.IntegerField(read_only = True)    #döngüye girmesin diye id 
    service = ServiceSerializers(read_only = True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_compulsory = serializers.BooleanField()

class AdditionalFeeSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    plan_id = serializers.IntegerField(read_only =True)
    name = serializers.CharField()
    price =serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False)#olmayada bilir demek

class SchoolPlanSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only =True)
    school_id = serializers.IntegerField(read_only = True)
    title = serializers.CharField()
    grade_level = serializers.CharField()
    description = serializers.CharField(required = False) #boş olabilir 
    cash_price = serializers.DecimalField(max_digits=10, decimal_places=2)     #max_digits ve decimal_places zorunludur decimalField da 
    installment_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    languages = LanguageSerializers(many = True)
    included_services = ServiceSerializers(many = True)

    planoption_set = PlanOptionSerializers(many = True)
    additionalfee_set = AdditionalFeeSerializers(many = True)


class SchoolImageSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    school_id = serializers.IntegerField() 
    image =serializers.ImageField()



class SchoolDetailSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    slug = serializers.SlugField()
    school_type = serializers.CharField()
    address = serializers.CharField()

    city = CitySerializers(read_only = True)
    district = DistrictSerializers(read_only = True)
    features = SchoolFeatureSerializers(many = True)
    #normalde schoolplan_set olması gerekitdi ama related_name yapdığımız için modelde 
    plans = SchoolPlanSerializers(many = True)
    images = SchoolImageSerializers(many = True)

