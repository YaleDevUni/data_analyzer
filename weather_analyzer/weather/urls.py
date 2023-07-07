from django.urls import path
from .views import fetch_weather_data
from .views import table_view

urlpatterns = [
    path('fetch-weather/<str:country>/',
         fetch_weather_data, name='fetch-weather'),
    path('table/', table_view, name='table'),
]
