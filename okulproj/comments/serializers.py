from rest_framework import serializers
from .models import Comment
from leads.models import Lead

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # Bu alan veritabanında yok, biz hesaplayıp ekliyoruz
    is_verified_parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'school', 'content', 'rating', 'created_at', 'is_verified_parent']
        #school yazmadık çünkü biz user ın hangi schoola yazacağını bilemeyiz user yazdık çünkü user kesindir 
        read_only_fields = ['id', 'user', 'created_at']

    def get_is_verified_parent(self, obj):
        # obj: Şu anki Yorum nesnesi
        # Yorumu yapan kişinin emaili ile, Yorum yapılan okulda 'SIGNED' (Kayıtlı) bir Lead var mı?
        user_email = obj.user.email
        school = obj.school
        
        # Lead tablosunda arama yapıyoruz
        is_parent = Lead.objects.filter(
            email=user_email, 
            school=school, 
            status=Lead.Status.SIGNED
        ).exists()
        
        return is_parent

    def create(self, validated_data):
        # Yorumu oluşturan kişi, o an giriş yapmış olan kullanıcıdır (request.user)
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)
    