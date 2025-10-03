from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название экскурсии', max_length=200, unique=True)
    short_description = models.TextField('Краткое описание экскурсии', default='', blank=True)
    long_description = HTMLField('Подробное описание экскурсии', default='', blank=True)

    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField('Фото', upload_to='places_images/')
    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.place.title} — фото {self.order}"