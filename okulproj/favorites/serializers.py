from rest_framework import serializers
from .models import Favorite
from schools.serializers import SchoolSerializers

class FavoriteSerializer(serializers.ModelSerializer):
    # OKUMA İÇİN: Okulun tüm detaylarını getirir (Nested Serializer)
    # read_only=True: Çünkü kayıt atarken kullanıcı bize koca bir okul objesi yollamaz, sadece ID yollar.
    # source='school': Bu alanın verisini 'school' ilişkisinden çek diyoruz.
    school_detail = SchoolSerializers(source='school', read_only=True)
    
    # OKUMA İÇİN: User'ın sadece adını/mailini gösterelim (Opsiyonel)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'school', 'school_detail', 'created_at']
        # Kayıt yaparken (POST) school zorunludur.
        # Okurken (GET) school_detail görünür.
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        # Kaydederken user'ı biz ekliyoruz (Token'dan gelen kişi)
        user = self.context['request'].user
        
        # Eğer kullanıcı aynı okulu tekrar favorilemeye çalışırsa hata verelim
        # (Gerçi Modelde UniqueTogether var ama burada da yakışıklı bir hata mesajı dönelim)
        school = validated_data['school']
        if Favorite.objects.filter(user=user, school=school).exists():
             raise serializers.ValidationError({"detail": "Bu okulu zaten favorilediniz."})

        return Favorite.objects.create(user=user, **validated_data)
