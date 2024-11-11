from django.shortcuts import render
import requests
from .forms import CityForm
from .models import City
from django.http import JsonResponse
import json


def index(request):
    api_key = 'd58ed7839ff5c87abed32f094cfb9967'  # Sign up at OpenWeatherMap for an API key
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            City.objects.create(name=city)

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city.name, api_key))
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city.name,
                'temperature': round(city_weather['main']['temp']),
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
            }
            weather_data.append(weather)

    context = {
        'weather_data': weather_data,
        'form': form,
    }
    return render(request, 'Weather/index.html')
