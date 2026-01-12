from django.db import models
from django.forms import CharField, DateTimeField
from schools.models import School, SchoolPlan, PlanOption
from core.models import BaseModel
# Create your models here.
class Lead(BaseModel):
    name = models.CharField("Başvuru Yapan Adı", max_length=128)
    surname = models.CharField("Başvuru Yapan Soyadı", max_length=128)
    phone_number = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    school_plan = models.ForeignKey(SchoolPlan, on_delete=models.CASCADE)
    plan_option = models.ManyToManyField(PlanOption, blank=True)

    time = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        NEW = "new"            
        UNREACHABLE = "unreachable"
        CONTACTED = "contacted"      
        MEETING = "meeting"
        SIGNED = "signed"     
        NEGATIVE = "negative"

    status = models.CharField(max_length=155, choices = Status.choices, default=Status.NEW)


    def __str__(self):
        return f"{self.name} {self.surname} - {self.school.name}"