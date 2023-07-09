from django.http import HttpResponse
from django.shortcuts import render
import requests
from .models import Weather
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr


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


def visualize_data(request):
    # Fetch data from the database
    weather_data = Weather.objects.all()

    # Create a pandas DataFrame
    df = pd.DataFrame(list(weather_data.values()))

    # Handling missing values
    # It might inproper to fill missing values with 0 or mean
    df.dropna()  # Remove rows with any missing value
    df.fillna(value=0)  # Fill missing values with 0
    # Fill missing values with mean
    df['temperature_c'].fillna(df['temperature_c'].mean(), inplace=True)
    # Fill missing values with mean
    df['uv'].fillna(df['uv'].mean(), inplace=True)
    # Handling duplicates
    df.drop_duplicates()  # Remove duplicate rows

    # Create the scatter plot with regression line
    plt.figure(figsize=(8, 5))
    sns.regplot(x='temperature_c', y='uv', data=df, color='skyblue')

    plt.xlabel('Temperature (°C)')
    plt.ylabel('UV Index')
    plt.title('UV Index by Temperature')
    plt.grid(True)
    plt.tight_layout()
    # Add labels for the regression line
    coef = np.polyfit(df['temperature_c'], df['uv'], deg=1)
    poly1d_fn = np.poly1d(coef)
    plt.annotate(f"UV = {coef[0]:.2f} * Temp + {coef[1]:.2f}",
                 xy=(df['temperature_c'].mean(), poly1d_fn(
                     df['temperature_c'].mean())),
                 xytext=(20, 20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))
    # Save the plot to an image file
    plot_file = 'static/images/plot.png'
    plt.savefig(plot_file)
    plt.close()

    # Render the DataFrame as an HTML table
    optional_fields = ['city', 'temperature_c', 'uv', 'last_updated']
    df_optional = df[optional_fields]
    optional_html_table = df_optional.to_html(index=False)
    html_table = df.to_html(index=False)

    # Pass the HTML table to the Django template context
    context = {'html_table': html_table,
               'optional_html_table': optional_html_table}
    return render(request, 'templates/visualize_data.html', context)


def analyze_data(request):
    # Fetch the data
    weather_data = Weather.objects.all()
    df = pd.DataFrame(list(weather_data.values()))

    # Handling missing values
    # It might inproper to fill missing values with 0 or mean
    df.dropna()  # Remove rows with any missing value
    df.fillna(value=0)  # Fill missing values with 0
    # Fill missing values with mean
    df['temperature_c'].fillna(df['temperature_c'].mean(), inplace=True)
    # Fill missing values with mean
    df['uv'].fillna(df['uv'].mean(), inplace=True)
    # Handling duplicates
    df.drop_duplicates()  # Remove duplicate rows

    # Calculate descriptive statistics
    temperature_stats = df['temperature_c'].describe()
    uv_stats = df['uv'].describe()

    # Calculate correlation
    correlation = df[['temperature_c', 'uv']].corr()
    correlation_coefficient = correlation.iloc[0, 1]

    # Perform hypothesis test
    correlation_test, p_value = pearsonr(df['temperature_c'], df['uv'])
    alpha = 0.05
    if p_value > alpha:
        hypothesis_result = "Fail to reject the null hypothesis"
    else:
        hypothesis_result = "Reject the null hypothesis"

    # Convert statistics and correlation to HTML tables
    temperature_table = temperature_stats.to_frame(
    ).transpose().to_html(index=False, classes='table')
    uv_table = uv_stats.to_frame().transpose().to_html(index=False, classes='table')
    correlation_table = correlation.to_html(classes='table')

    context = {
        'temperature_table': temperature_table,
        'uv_table': uv_table,
        'correlation_table': correlation_table,
        'correlation_coefficient': correlation_coefficient,
        'p_value': p_value,
        'hypothesis_result': hypothesis_result
    }

    return render(request, 'templates/analyze_data.html', context)
