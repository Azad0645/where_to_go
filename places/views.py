from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
                "detailsUrl": f"/places/{place.id}.json"
            }
        })

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, 'index.html', {
        'places_geojson': json.dumps(places_geojson, ensure_ascii=False)
    })


def place_json(request, pk):
    place = get_object_or_404(Place.objects.prefetch_related('images'), pk=pk)

    data  = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude
        }
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
