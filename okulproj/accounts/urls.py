from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterAPIView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    # 2. Giriş Yap & Token Al(Hazır gelir)
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 3. Token Yenile (Hazır Gelir)
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

#Buralar eski branch da vardı api iletişiminde olmayacak 
#template_name araması gereken yeri direkt vermeyi yarar template/accounts/login.html de arıyıcak 
#Template_view da render eder direkt sayfa ver gösteriym der  yani view da method açıp renderlamak 
