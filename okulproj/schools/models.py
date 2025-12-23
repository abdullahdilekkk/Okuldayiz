from pyexpat import model
from django.conf import settings
from django.db import models
from django.forms import CharField, ChoiceField
from accounts.models import City, District

# Create your models here.

class SchoolFeature(models.Model):
    title = models.CharField("Özellik Adı", max_length=50)

    def __str__(self):
        return self.title

class Language(models.Model):
    name = models.CharField("Dil Adı", max_length=156)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField("Servis Adı", max_length=156)
    icon = models.CharField("İkon Kodu", max_length=50, blank=True)

    def __str__(self):
        return self.name

class School(models.Model):

    class SchoolType(models.TextChoices):
        PRIVATE = "ozel", "Özel Okul / Kolej"
        PUBLIC = "devlet", "Devlet Okulu"


    #sahibi custom user dan çekilecek 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schools")

    #okulun temel bilgileri
    name = models.CharField("Okul Adı", max_length=256)
    slug = models.SlugField("URL Yolu", unique=True)
    description = models.TextField("Hakkında", blank=True)
    school_type = models.CharField("Okul Türü", choices=SchoolType.choices, max_length=126)
    lead_limit = models.PositiveIntegerField("Öğrenci Kotası", default=0)
    is_active = models.BooleanField(default=True)

    #konum bilgileri 
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    address = models.TextField("Açık Adres")

    features = models.ManyToManyField(SchoolFeature, blank =True)


    created_at = models.DateTimeField(auto_now_add=True) # İlk oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)     # Son güncellenme tarihi

    def __str__(self):
        return self.name

class SchoolPlan(models.Model):
    class GradeLevel(models.TextChoices):
        KRES = 'kres', 'Kreş'
        ANAOKULU = 'anaokulu', 'Anaokulu'
        ILKOKUL = 'ilkokul', 'İlkokul'
        ORTAOKUL = 'ortaokul', 'Ortaokul'
        LISE = 'lise', 'Lise'
        UNIVERSITE = 'universite', 'Üniversite'


    school = models.ForeignKey(School, related_name="plans", on_delete=models.CASCADE)
    title = models.CharField("Plan Başlığı", max_length=256)
    grade_level = models.CharField("Eğitim Kademesi", choices=GradeLevel.choices, max_length=20)


    languages = models.ManyToManyField(Language, blank=True)


    description = models.TextField("Ekstra Açıklama", blank=True)

    #standart paket fiyatı peşin/taksitli
    cash_price = models.DecimalField("Peşin Fiyat", max_digits=10, decimal_places=2)
    installment_price = models.DecimalField("Taksitli Fiyat (Liste Fiyatı)", max_digits=10, decimal_places=2)

    included_services = models.ManyToManyField(Service, blank=True, verbose_name="Fiyata Dahil Standart Hizmetler")


    def __str__(self):
        return f"{self.school}-{self.title}"
    
class PlanOption(models.Model):

    plan = models.ForeignKey(SchoolPlan, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


    price = models.DecimalField("Ek Ücret", max_digits=10, decimal_places=2)
    is_compulsory = models.BooleanField("Zorunlu mu?", default=False) # Bazı okullarda yemek zorunlu olabilir


    def __str__(self):
        durum = "Zorunlu" if self.is_compulsory else "İsteğe Bağlı"
        return f"{self.service.name} (+{self.price} TL) - {durum}"
    
class AdditionalFee(models.Model):
    """
    Eğitim ve hizmet dışındaki diğer giderler.
    Örn: Kırtasiye, Kıyafet, Kayıt Yenileme Bedeli
    """
    plan = models.ForeignKey(SchoolPlan, on_delete=models.CASCADE)
    name = models.CharField("Gider Adı", max_length=100)
    price = models.DecimalField("Ücret", max_digits=10, decimal_places=2)
    description = models.TextField("Açıklama", blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.price} TL)"
    
class SchoolImage(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Okul Görseli", upload_to="school_images/")
    
    def __str__(self):
        return f"{self.school.name} - Resim"