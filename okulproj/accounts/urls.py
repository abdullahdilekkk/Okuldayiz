from django.urls import path
from django.contrib.auth import views as DefaultAuth
from django.views.generic import TemplateView 

app_name = "accounts"

urlpatterns = [
    path("login/", DefaultAuth.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    
    # 2. GÜVENLİKÇİYİ ARADAN ÇIKARDIK, DİREKT ALETİ KULLANDIK
    path("profile/", TemplateView.as_view(template_name="accounts/profile.html"), name="profile"),
    
    # 3. PARANTEZİ UNUTMA (LogoutView bir sınıf olduğu için () gerekir)
    path("logout/", DefaultAuth.LogoutView.as_view(), name="logout")
]
#Djangonun default auth yapısını kullanıyorum

#as_view onu bir methoda çevirir yoksa LoginView bir sınıftır 

#template_name araması gereken yeri direkt vermeyi yarar template/accounts/login.html de arıyıcak 

#Template_view da render eder direkt sayfa ver gösteriym der  yani view da method açıp renderlamak 
