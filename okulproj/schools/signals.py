from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Min, Max
from .models import SchoolPlan

@receiver([post_save, post_delete], sender=SchoolPlan)
def update_school_prices(sender, instance, *args, **kwargs):

    school = instance.school

    aggregates = school.plans.aggregate(
        min_price = Min("cash_price"),
        max_price = Max("cash_price")
    )

    school.min_price = aggregates["min_price"] or 0
    school.max_price = aggregates["max_price"] or 0

    school.save(update_fields = ["min_price", "max_price"])