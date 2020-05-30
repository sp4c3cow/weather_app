from django.shortcuts import render
from .forms import CityForm
import requests
from .models import City

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=67e7b776de43fc6fd48c720d163a6bfc'
    cities = City.objects.all()
    form = CityForm()

    if request.method == 'POST': 
        form = CityForm(request.POST)
        form.save()
    
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        
        weather = {
            'city': city,
            'temp': city_weather['main']['temp'],
            'icon': city_weather['weather'][0]['icon'],
            'description': city_weather['weather'][0]['description']
        }

        weather_data.append(weather)
        
    context = {
        'weather_data': weather_data,
        'form' : form
    }
    
    return render(request, 'weather/index.html', context)