from atexit import register
from pyexpat import model
from django.contrib import admin
from .models import SchoolFeature, Language, Service, School, SchoolPlan, PlanOption, AdditionalFee, SchoolImage
# Register your models here.

class SchoolImageInline(admin.TabularInline):
    model = SchoolImage
    extra = 1   
    classes = ["collapse"]  

class PlanOptionInline(admin.TabularInline):
    model = PlanOption
    extra = 1
    autocomplete_fields = ['service']

class AdditionalFeeInline(admin.TabularInline):
    model = AdditionalFee
    extra = 1




@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "school_type", "city", "district", "owner")
    list_filter = ('school_type', 'city')
    search_fields = ("name",)
    inlines = (SchoolImageInline, )
    filter_horizontal = ('features',)

    prepopulated_fields = {
        "slug" : ("name",)
    }  #oto slug üretir 



@admin.register(SchoolPlan)
class SchoolPlanAdmin(admin.ModelAdmin):
    list_display = ("school", "title", "grade_level")
    list_filter = ('school', )
    search_fields = ('title', 'school__name')
    inlines = (PlanOptionInline, AdditionalFeeInline)
    filter_horizontal = ('languages', "included_services")



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ('name',)


@admin.register(SchoolFeature)
class SchoolFeatureAdmin(admin.ModelAdmin):
    search_fields = ('title',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name',)