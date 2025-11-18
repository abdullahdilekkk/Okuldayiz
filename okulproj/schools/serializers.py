from rest_framework import serializers
from .models import School
from accounts.serializers import CitySerializers, DistrictSerializers
#python sürümü sorunlarından dolayı burayı alt sınıf olan Serializer e geçtik 
class SchoolSerializers(serializers.Serializer):
    id = serializers.ImageField(read_only =True)
    name = serializers.CharField()
    slug = serializers.SlugField()
    school_type = serializers.CharField()
    address = serializers.CharField()

    city = CitySerializers(read_only=True)
    district = DistrictSerializers(read_only=True)



    # model = School
    # fields = ["id", "name", "slug", "school_type", "city", "district", "address"]