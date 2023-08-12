from django.shortcuts import render
from django.conf import settings
import requests
import datetime
import os

def index(request):
    # Get the API key from Django settings
    api_key = settings.OPEN_WEATHER_MAP_API_KEY
    
    # Check if the request method is POST (i.e., user submitted the form)
    if request.method == 'POST':
        # Log the POST data for debugging purposes
        print(request.POST) 

        # Extract the first city name from the POST data
        city1 = request.POST['city1']

        # Construct URLs for fetching current weather and forecast for the first city
        current_weather_url1 = f'https://api.openweathermap.org/data/2.5/weather?q={city1}&appid={api_key}'
        forecast_url1 = f'https://api.openweathermap.org/data/2.5/forecast?q={city1}&appid={api_key}'

        # Fetch weather and forecast for the first city
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url1, forecast_url1)

        # Attempt to extract the second city name from the POST data (if provided)
        city2 = request.POST.get('city2', None)

        # If a second city is provided, fetch its weather and forecast
        if city2:
            current_weather_url2 = f'https://api.openweathermap.org/data/2.5/weather?q={city2}&appid={api_key}'
            forecast_url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city2}&appid={api_key}'
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url2, forecast_url2)
        else:
            weather_data2, daily_forecasts2 = None, None

        # Create a context dictionary to pass data to the template
        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        # Render the index page with the fetched data
        return render(request, 'weather_app/index.html', context)
    else:
        # If it's not a POST request, simply render the index page without data
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather data for the city
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # Check for errors in the response
    if 'coord' not in response:
        print("Error fetching current weather for city:", city)
        print(response)
        return None, None

    # Fetch 5-day forecast data for the city
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    # Print the forecast response for debugging purposes
    print(forecast_response)

    # Process the current weather data
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),  # Convert from Kelvin to Celsius
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # Process the 5-day forecast data (which is provided in 3-hourly intervals)
    daily_forecasts = []

    # Loop over the forecast data in 8-data-point intervals (representing 24 hours)
    for i in range(0, 40, 8):
        daily_data = forecast_response['list'][i]
        day = datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A')
        
        # Calculate min and max temperatures for the day
        min_temp = round(min(item['main']['temp_min'] for item in forecast_response['list'][i:i+8]) - 273.15, 2)
        max_temp = round(max(item['main']['temp_max'] for item in forecast_response['list'][i:i+8]) - 273.15, 2)
        
        # Extract weather description and icon for the day
        description = daily_data['weather'][0]['description']
        icon = daily_data['weather'][0]['icon']

        # Add the processed data for the day to the daily_forecasts list
        daily_forecasts.append({
            'day': day,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon,
        })

    return weather_data, daily_forecasts
