from django.db import models
from django.contrib.auth.models import AbstractUser 
#custom bir user modeli için miras alıyorum



#User, Group, Permission, UserManager } django.contrib.auth.models den gelir ama username 
#daha aşağı katmanda özelleştirilir bu yüzden django.contrib.auth.base_user
from django.contrib.auth.base_user import BaseUserManager 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):    # self, USERNAME_FIELD de ne varsa ,REQUIRED_FIELDS varsa ,password
        if not email:
            raise ValueError("Email zorunludur")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Süper kullanıcı için is_staff=True olmalı")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Süper kullanıcı için is_superuser=True olmalı")

        return self.create_user(email, password, **extra_fields)




class City(models.Model):
    name = models.CharField(max_length=256, unique=True)
    plate_no = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["plate_no"] #sıralama için


    def __str__(self):
       return self.name
        

class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=256)

    class Meta:
        unique_together = ["city", "name"]  #beraber benzersiz olur 
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []        


    objects = CustomUserManager() #bu modelde kullanıcı oluşturma, sorgulama ve superuser işlemlerini bu manager yönetsin

    
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"    # db de görünen , Kullnıcıya görünen
        USER = "user" , "User"
        OWNER = "owner" , "Okul Sahibi"
    username = None
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=255,unique=True)   #Tek email = True
    phone_number = models.CharField(max_length=256)
    role = models.CharField(max_length=155, default=Role.USER, choices=Role.choices)
    #default olarak User atar seçenekler ise sadece Role sınıfındakilerdir 


    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)   #olamzsa kaydım NULL yap beni direkt silme demek
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)

    verified = models.BooleanField(default=False)
    #diğer alanlar AbstructBaseUser dan geliyor 


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    