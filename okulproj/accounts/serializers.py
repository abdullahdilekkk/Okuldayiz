from os import name
from rest_framework import serializers


class CitySerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    plate_no = serializers.IntegerField()


class DistrictSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    city_id = serializers.IntegerField() #drf direkt city_id den city i alabilir 
