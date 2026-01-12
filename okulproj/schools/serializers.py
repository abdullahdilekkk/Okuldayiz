from rest_framework import serializers
from .models import AdditionalFee, Language, School, SchoolFeature
from accounts.serializers import CitySerializers, DistrictSerializers, CityRelatedField, DistrictRelatedField
from accounts.models import City, District

class SchoolFeatureSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField()

class SchoolFeatureRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return SchoolFeatureSerializers(value).data
    
class SchoolSerializers(serializers.ModelSerializer):
    
    city = CityRelatedField(queryset = City.objects.all(), required = True, allow_null = False)
    district = DistrictRelatedField(queryset = District.objects.all(), required = True, allow_null = False)
    features = SchoolFeatureRelatedField(queryset = SchoolFeature.objects.all(), many = True, required = False)

    class Meta:        
        model = School
        fields = [
            "id",
            "name",
            "owner",
            "school_type",
            "city",
            "district",
            "description",
            "slug",
            "features",
            "created_at",
            "updated_at"
            ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):

        city = attrs.get('city')
        district = attrs.get('district')
        if city and district:
            if district.city != city:
                raise serializers.ValidationError({"district": "Seçtiğiniz ilçe, seçtiğiniz şehre ait değil!"})
        return attrs


class LanguageSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()

class ServiceSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    icon = serializers.CharField()


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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")   

        if request is None or not request.user.is_authenticated:
            data.pop("plans", None)

        return data
    
    
# # View tarafında (Django bunu senin için otomatik yapar):
# serializer = SchoolDetailSerializers(
#     instance=okul_objesi, 
#     context={'request': request}  # <-- İŞTE BU SATIR!

class SchoolUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["name", "description", "school_type", "city", "district", "address", "features"]



    def validate(self, attrs):
        
        request_city = attrs.get("city")
        request_district = attrs.get("district")

        if "city" in attrs:
            final_city = request_city
        else:
            final_city = self.instance.city
        
        if "district" in attrs:
            final_district = request_district
        else:
            final_district = self.instance.district

        if final_city and final_district:
            if final_district.city != final_city:
                raise serializers.ValidationError({
                    "district": f"Hata! '{final_district.name}' ilçesi, '{final_city.name}' şehrine bağlı değildir."
                })
            
        return attrs
    
    def to_representation(self, instance):
        response = super().to_representation(instance)

        if instance.city:
            response['city'] = {
                "id": instance.city.id,
                "name": instance.city.name
            }
    
        if instance.district:
            response['district'] = {
                "id": instance.district.id,
                "name": instance.district.name
            }

        if instance.features.exists():
            response['features'] = [
                {"id": f.id, "title": f.title, "icon": f.icon if hasattr(f, 'icon') else None} 
                for f in instance.features.all()
            ]
        else:
            response['features'] = []

        return response