from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from schools.models import School

class Comment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("Yorum İçeriği")
    rating = models.PositiveSmallIntegerField(
        "Puan", 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    
    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.school} ({self.rating})"
