import requests

LOCATION_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


def search_location(search_str):
    response = requests.get(
        LOCATION_API_URL,
        params={
            'name': search_str,
            'language': 'ru'
        }
    )
    return response.json().get('results', [])


def get_weather(latitude, longitude):
    response = requests.get(
        WEATHER_API_URL,
        params={
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max',
            'wind_speed_unit': 'ms'
        }
    )
    return response.json(), response.status_code
