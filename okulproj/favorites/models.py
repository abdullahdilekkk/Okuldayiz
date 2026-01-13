from django.db import models
from django.conf import settings
from schools.models import School
from core.models import BaseModel



class Favorite(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="favorites")

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        verbose_name = "Favorite"
        unique_together = ["user", "school"]

    def __str__(self):
        return f"{self.user} favorited {self.school}"
