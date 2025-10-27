from django.db import models
from django.contrib.auth.models import AbstractUser
#custom bir user modeli için miras alıyorum


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
    class Role(models.TextChoices):
        ADMİN = "admin", "Admin"    # db de görünen , Kullnıcıya görünen
        USER = "user" , "User"
        OWNER = "owner" , "Okul Sahibi"

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    