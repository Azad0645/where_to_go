import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL до JSON файла')

    def handle(self, *args, **options):
        url = options['url']

        response = requests.get(url)
        if not response.ok:
            self.stderr.write(self.style.ERROR(
                f"Ошибка {response.status_code} при загрузке JSON: {url}"
            ))
            return

        place_data = response.json()

        place, created = Place.objects.get_or_create(
            title=place_data ['title'],
            defaults={
                'short_description': place_data.get('description_short', ''),
                'long_description': place_data.get('description_long', ''),
                'latitude': float(place_data['coordinates']['lat']),
                'longitude': float(place_data['coordinates']['lng']),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Создано место: {place.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Место уже существует: {place.title}"))

        deleted, _ = place.images.all().delete()
        if deleted:
            self.stdout.write(self.style.WARNING(f'Удалены старые фото: {deleted}'))

        for order, img_url in enumerate(place_data.get('imgs', [])):
            img_response = requests.get(img_url)
            if not img_response.ok:
                self.stderr.write(self.style.ERROR(
                    f"Ошибка {img_response.status_code} при загрузке изображения: {img_url}"
                ))
                continue

            image_name = os.path.basename(img_url)
            PlaceImage.objects.create(
                place=place,
                order=order,
                image=ContentFile(img_response.content, name=image_name)
            )