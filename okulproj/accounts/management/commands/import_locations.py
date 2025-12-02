from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from accounts.models import City, District

class Command(BaseCommand):

    help = "Json veri formatı ile Turkiyedeki illeri sisteme yükler "

    def turkce_fix(self ,text):
        text = text.replace("I", "ı").replace("İ", "i")
        return text.lower().title()


    def handle(self, *args, **kwargs):
        
        file_path_city = os.path.join(settings.BASE_DIR, 'json_datas', 'cities_of_turkey.json')
        file_path_district = os.path.join(settings.BASE_DIR, 'json_datas', 'districts_of_turkey.json')

        with open(file = file_path_city, encoding='utf-8') as file:
            data_city = json.load(file)
            
        with open(file = file_path_district, encoding='utf-8') as file:
            data_district = json.load(file)

        for item in data_city:
            City.objects.update_or_create(
                plate_no=item["id"],
                defaults={
                    "name": item["name"],
                    "plate_no": item["id"]
                }
            )
        for index_district in data_district:
            try:
                object_of_city = City.objects.get(name__iexact = self.turkce_fix(index_district["name"]))

                for dist in index_district["districts"]:
                    District.objects.update_or_create(
                        city = object_of_city,
                        name=dist["name"],
                        defaults={
                            "name":dist["name"],
                            "city":object_of_city
                        }
                    )
            except City.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Şehir Bulunamadı (Atlanıyor): {index_district['name']}"))
                continue
                


