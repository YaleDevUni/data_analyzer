from django.urls import path
from .views import visualize_data, analyze_data, fetch_weather_data

urlpatterns = [
    path('fetch-weather/<str:country>/',
         fetch_weather_data, name='fetch-weather'),
    path('visualize-data/', visualize_data, name='visualize-data'),
    path('analyze-data/', analyze_data, name='analyze-data'),
]
