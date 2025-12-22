from django.shortcuts import render
import rest_framework.exceptions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserProfileSerializer, VerifyInputSerializer
from .models import User
import rest_framework
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainSerializer


class MyLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer
    # Memura talimat veriyoruz: "Standart serializer'ı değil, benim yazdığımı kullan."

class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyInputSerializer
    def post(self, request):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")
        user = User.objects.filter(email = email).first()

        if user is None:
            raise rest_framework.exceptions.ValidationError({"user":"user bulunamadı"})
        
        if str(user.verification_code) != str(verification_code):
            raise rest_framework.exceptions.ValidationError({"code":"code eşleşmedi"})
        else:
            user.is_active = True
            user.verification_code = None
            user.save()
            return Response({"detail": "Başarılı"}, status=status.HTTP_200_OK)



class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
    