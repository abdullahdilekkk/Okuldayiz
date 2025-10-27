from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as MirasUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(MirasUserAdmin):
#alt sınıftsn miras aldık adını aynı kullanmak için as dedik

    list_display = ["username", "email","role", "is_active"]
    #tablo halinde hangi sütunları göstereceğini belirler
    search_fields = ("email","first_name","last_name","phone_number")

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email","password")}),
        ("Kişisel", {"fields": ("first_name","last_name")}),
        ("Rol & Yetki", {"fields": ("role","is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Önemli Tarihler", {"fields": ("last_login","date_joined")}))
    
    add_fieldsets = (
        (None, {"fields": ("email","password1","password2","role","is_staff","is_active")}),
    )
    #custom user yaptığımız için zorunlu
