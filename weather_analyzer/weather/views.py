from django.http import HttpResponse
from django.shortcuts import render
import requests
from .models import Weather
import pandas as pd


def fetch_weather_data(request, country):
    api_url = f"http://api.weatherapi.com/v1/current.json?key=24ec30290b2e4df095d65708230707&q={country}&aqi=no"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        location = data["location"]
        current = data["current"]

        weather = Weather(
            city=location["name"],
            region=location["region"],
            country=location["country"],
            temperature_c=current["temp_c"],
            temperature_f=current["temp_f"],
            is_day=current["is_day"],
            condition_text=current["condition"]["text"],
            condition_icon=current["condition"]["icon"],
            wind_mph=current["wind_mph"],
            wind_kph=current["wind_kph"],
            wind_degree=current["wind_degree"],
            wind_dir=current["wind_dir"],
            pressure_mb=current["pressure_mb"],
            pressure_in=current["pressure_in"],
            precip_mm=current["precip_mm"],
            precip_in=current["precip_in"],
            humidity=current["humidity"],
            cloud=current["cloud"],
            feelslike_c=current["feelslike_c"],
            feelslike_f=current["feelslike_f"],
            visibility_km=current["vis_km"],
            visibility_miles=current["vis_miles"],
            uv=current["uv"],
            gust_mph=current["gust_mph"],
            gust_kph=current["gust_kph"],
            last_updated=current["last_updated"],
        )
        weather.save()

        weather_data = {
            'city': location['name'],
            'region': location['region'],
            'country': location['country'],
            'temperature_c': current['temp_c'],
            'temperature_f': current['temp_f'],
            'is_day': current['is_day'],
            'condition_text': current['condition']['text'],
            'condition_icon': current['condition']['icon'],
            'wind_mph': current['wind_mph'],
            'wind_kph': current['wind_kph'],
            'wind_degree': current['wind_degree'],
            'wind_dir': current['wind_dir'],
            'pressure_mb': current['pressure_mb'],
            'pressure_in': current['pressure_in'],
            'precip_mm': current['precip_mm'],
            'precip_in': current['precip_in'],
            'humidity': current['humidity'],
            'cloud': current['cloud'],
            'feelslike_c': current['feelslike_c'],
            'feelslike_f': current['feelslike_f'],
            'visibility_km': current['vis_km'],
            'visibility_miles': current['vis_miles'],
            'uv': current['uv'],
            'gust_mph': current['gust_mph'],
            'gust_kph': current['gust_kph'],
            'last_updated': current['last_updated'],
        }
        return render(request, 'templates/weather.html', {'weather_data': weather_data})
    else:
        return render(request, 'templates/invalid_weather.html')


def table_view(request):
    qs = Weather.objects.all()
    context = {'qs': qs}
    return render(request, 'templates/table.html', context)
