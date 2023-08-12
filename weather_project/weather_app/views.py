from django.shortcuts import render
from django.conf import settings
import requests
import datetime
import os



def index(request):
    api_key = settings.OPEN_WEATHER_MAP_API_KEY
    
    if request.method == 'POST':
        print(request.POST) 
        city1 = request.POST['city1']
        current_weather_url1 = f'https://api.openweathermap.org/data/2.5/weather?q={city1}&appid={api_key}'
        forecast_url1 = f'https://api.openweathermap.org/data/2.5/forecast?q={city1}&appid={api_key}'

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url1, forecast_url1)

        city2 = request.POST.get('city2', None)
        if city2:
            current_weather_url2 = f'https://api.openweathermap.org/data/2.5/weather?q={city2}&appid={api_key}'
            forecast_url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city2}&appid={api_key}'
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url2, forecast_url2)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()

    if 'coord' not in response:
        print("Error fetching current weather for city:", city)
        print(response)
        return None, None

    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    # Print the forecast response to diagnose potential issues
    print(forecast_response)

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # Process 5-day forecast data from 3-hourly intervals:
    daily_forecasts = []
    for i in range(0, 40, 8):  # There are 40 data points (5 days * 8 data points/day)
        daily_data = forecast_response['list'][i]
        day = datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A')
        min_temp = round(min(item['main']['temp_min'] for item in forecast_response['list'][i:i+8]) - 273.15, 2)
        max_temp = round(max(item['main']['temp_max'] for item in forecast_response['list'][i:i+8]) - 273.15, 2)
        description = daily_data['weather'][0]['description']
        icon = daily_data['weather'][0]['icon']
        daily_forecasts.append({
            'day': day,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon,
        })
    print(forecast_response)

    return weather_data, daily_forecasts
