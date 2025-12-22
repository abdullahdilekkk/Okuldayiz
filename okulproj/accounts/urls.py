from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterAPIView, UserProfileAPIView, VerifyEmailView
from .views import MyLoginView
app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    # 2. Giriş Yap & Token Al(Hazır gelir)
    path("login/", MyLoginView.as_view(), name="token_obtain_pair"),
    # 3. Token Yenile (Hazır Gelir)
    path("me/", UserProfileAPIView.as_view(), name="user_profile"),
    path("verify-email/", VerifyEmailView.as_view(), name = "verify-email"),
]

#Buralar eski branch da vardı api iletişiminde olmayacak 
#template_name araması gereken yeri direkt vermeyi yarar template/accounts/login.html de arıyıcak 
#Template_view da render eder direkt sayfa ver gösteriym der  yani view da method açıp renderlamak 
