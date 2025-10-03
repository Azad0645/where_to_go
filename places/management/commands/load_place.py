import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from main.models import Place, PlaceImage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL до JSON файла')

    def handle(self, *args, **options):
        url = options['url']

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        place, created = Place.objects.get_or_create(
            title=data['title'],
            defaults={
                'description_short': data.get('description_short', ''),
                'description_long': data.get('description_long', ''),
                'latitude': float(data['coordinates']['lat']),
                'longitude': float(data['coordinates']['lng']),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Создано место: {place.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Место уже существует: {place.title}"))

        for order, img_url in enumerate(data.get('imgs', [])):
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            image_name = os.path.basename(img_url)

            PlaceImage.objects.create(
                place=place,
                order=order,
                image=ContentFile(img_response.content, name=image_name)
            )