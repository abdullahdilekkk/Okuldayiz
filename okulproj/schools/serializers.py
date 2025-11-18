from attr import fields
from rest_framework import serializers
from .models import School

#python sürümü sorunlarından dolayı burayı alt sınıf olan Serializer e geçtik 
class SchoolSerializers(serializers.Serializer):
    id = serializers.ImageField(read_only =True)
    name = serializers.CharField()
    slug = serializers.SlugField()
    school_type = serializers.CharField()
    address = serializers.CharField()

    # Şehir ve ilçe şimdilik sadece ID olarak dönecek
    city_id = serializers.IntegerField(read_only=True)
    district_id = serializers.IntegerField(read_only=True)




    # model = School
    # fields = ["id", "name", "slug", "school_type", "city", "district", "address"]