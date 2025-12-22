from django.contrib import admin
from .models import Lead
# Register your models here.
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'surname', 
        'school', 
        'status', 
        'phone_number', 
        'time'
    ]
    list_display_links = ['name', 'surname']
    search_fields = ['name', 'surname', 'phone_number', 'email']
    list_per_page = 20
    list_editable = ['status']
