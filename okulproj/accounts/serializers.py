from rest_framework import serializers
from .models import User, City, District
import random
from django.db import transaction   #atomic işlem yapmak için 
import logging
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class VerifyInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.IntegerField()
    
class CitySerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    plate_no = serializers.IntegerField()


class DistrictSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    city_id = serializers.IntegerField() #drf direkt city_id den city i alabilir 

logger = logging.getLogger(__name__)
class UserRegisterSerializer(serializers.ModelSerializer,):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    
    city = serializers.CharField()
    district = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone_number", "first_name", "last_name", "role", "city", "district")

    def validate(self, attrs):
        city_name = attrs.get('city')
        district_name = attrs.get('district')

        if city_name:
            try:
                city_obj = City.objects.get(name__iexact=city_name)
                attrs['city'] = city_obj 
            except City.DoesNotExist:
                raise serializers.ValidationError({"city": "Böyle bir şehir bulunamadı."})

        if district_name:
            if 'city' not in attrs or isinstance(attrs['city'], str):
                 pass
            else:
                city_obj = attrs['city'] # Yukarıda bulduğumuz şehir objesi
                try:
                    district_obj = District.objects.get(name__iexact=district_name, city=city_obj)
                    attrs['district'] = district_obj
                except District.DoesNotExist:
                    raise serializers.ValidationError({
                        "district": f"{district_name}, {city_obj.name} ilinde bulunamadı!"
                    })

        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        with transaction.atomic():
            user = User.objects.create_user(password = password,is_active = False ,**validated_data)
            user.verification_code = random.randint(100000, 999999)
            user.save()

            send_mail(
                subject="Okuldayız - Doğrulama Kodu",
                message=f'Merhaba {user.first_name}, doğrulama kodun: {user.verification_code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )



            logger.info(f"Kod gönderildi: {user.verification_code}")
            return user

class CityRelatedField(serializers.PrimaryKeyRelatedField):
    def use_pk_only_optimization(self):
        return False
    def to_representation(self, value):
        return CitySerializers(value).data

class DistrictRelatedField(serializers.PrimaryKeyRelatedField):
    def use_pk_only_optimization(self):
        return False
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
            "city",
            "district",
            "role"
            ]
        read_only_fields = ["email", "role"]

class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        # First name ve Last name birleştirip tam ad yapalım
        token['full_name'] = f"{user.first_name} {user.last_name}"
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["name"] = f"{self.user.first_name} {self.user.last_name}"
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "city", "district"]

    def validate(self, attrs):
        city = attrs.get("city")
        district = attrs.get("district")
        
        if city and district:
            if district.city != city:
                raise serializers.ValidationError({
                    "district": f"Seçilen ilçe ({district.name}), seçilen şehre ({city.name}) ait değil!"
                })
            

        return attrs
    

    def to_representation(self, instance):
        response = super().to_representation(instance)

        if instance.city:
            response["city"] = {
                "id": instance.city.id,
                "name": instance.city.name
            }

        if instance.district:
            response['district'] = {
                "id": instance.district.id,
                "name": instance.district.name
            }

        return response