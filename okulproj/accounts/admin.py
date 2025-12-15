from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as MirasUserAdmin
from .models import City, District, User
from django.contrib.auth.forms import UserCreationForm as MirasUserCreationForm
from django.contrib.auth.forms import UserChangeForm as MirasUserChangeForm


class UserCreationForm(MirasUserCreationForm):  #admin panelinde (veya custom bir register sayfasında) yeni kullanıcı oluşturmak için kullanılır.
    class Meta:
        model = User    #Cutom yaptığım User
        fields = ("email",)     #password1 ve password2 alanları kodla ekleniyor (__init__ içinde) miras aldığı metadan 



class UserChangeForm(MirasUserChangeForm):  #var olan kullanıcıları düzenlemek için kullanılır.
    class Meta:
        model = User
        fields = ("email","first_name","last_name","phone_number","role")





@admin.register(User)
class UserAdmin(MirasUserAdmin):
#alt sınıftsn miras aldık adını aynı kullanmak için as dedik

    add_form = UserCreationForm
    form = UserChangeForm
    model = User


    list_display = ["email","role", "is_active"]
    #tablo halinde hangi sütunları göstereceğini belirler
    search_fields = ("email","first_name","last_name","phone_number")

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email","password","verification_code")}),
        ("Kişisel", {"fields": ("first_name","last_name")}),
        ("Rol & Yetki", {"fields": ("role","is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Önemli Tarihler", {"fields": ("last_login","date_joined")}))
    
    add_fieldsets = (
        (None, {"fields": ("email","password1","password2","role","is_staff","is_active")}),
    )
    #custom user yaptığımız için zorunlu


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "plate_no")
    search_fields = ('name',)
    ordering = ('plate_no',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("city", "name")
    list_filter = ('city',) # Yan tarafta şehre göre filtreleme çıkar
    search_fields = ('name',)
    autocomplete_fields = ("city",)  #şehre göre arama yapmayı sağlar