from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Place
import json


def index(request):
    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": str(place.id),
                "detailsUrl": reverse('place_json', args=[place.id])
            }
        })

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, 'index.html', {
        'places_geojson':  places_geojson
    })


def place_json(request, pk):
    place = get_object_or_404(Place.objects.prefetch_related('images'), pk=pk)

    place_data  = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude
        }
    }

    return JsonResponse(place_data, json_dumps_params={'ensure_ascii': False})