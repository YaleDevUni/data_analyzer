from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100, primary_key=True)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    temperature_c = models.FloatField()
    temperature_f = models.FloatField()
    is_day = models.BooleanField()
    condition_text = models.CharField(max_length=100)
    condition_icon = models.CharField(max_length=200)
    wind_mph = models.FloatField()
    wind_kph = models.FloatField()
    wind_degree = models.IntegerField()
    wind_dir = models.CharField(max_length=10)
    pressure_mb = models.FloatField()
    pressure_in = models.FloatField()
    precip_mm = models.FloatField()
    precip_in = models.FloatField()
    humidity = models.IntegerField()
    cloud = models.IntegerField()
    feelslike_c = models.FloatField()
    feelslike_f = models.FloatField()
    visibility_km = models.FloatField()
    visibility_miles = models.FloatField()
    uv = models.FloatField()
    gust_mph = models.FloatField()
    gust_kph = models.FloatField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city
