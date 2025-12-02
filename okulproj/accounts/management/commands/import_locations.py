from django.core.management.base import BaseCommand

from django.conf import settings
import os, json
from accounts.models import City 

class Command(BaseCommand):

    help = "Json veri formatı ile Turkiyedeki illeri sisteme yükler "

    def handle(self, *args, **kwargs):
        
        file_path = os.path.join(settings.BASE_DIR,'json_datas', 'cities_of_turkey.json')

        with open(file = file_path, encoding='utf-8') as file:
            data = json.load(file)

        for index in data:
            City.objects.update_or_create(
                plate_no = index["id"],
                defaults = {
                    "name" : index["name"],
                    "plate_no" :index["id"]
                })


