from rest_framework import serializers
from .models import User


class CitySerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    plate_no = serializers.IntegerField()


class DistrictSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    city_id = serializers.IntegerField() #drf direkt city_id den city i alabilir 


class UserRegisterSerializer(serializers.ModelSerializer,):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("id", "email", "password", "phone_number", "first_name", "last_name", "role", "city", "district")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password = password, **validated_data)
        return user