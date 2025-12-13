from rest_framework import serializers
from .models import User, City, District


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

class CityRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return CitySerializers(value).data

class DistrictRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return DistrictSerializers(value).data
    
class UserProfileSerializer(serializers.ModelSerializer):
    city = CityRelatedField(queryset=City.objects.all(), required=False, allow_null=True)
    district = DistrictRelatedField(queryset=District.objects.all(), required=False, allow_null=True)


    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "city", "city_id",
            "district", "district_id",
            "role"
            ]
        read_only_fields = ["email", "role"]

