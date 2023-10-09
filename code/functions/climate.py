import json
import os
import requests

# API Keys 
# 1. [IQAir](https://www.iqair.com/dashboard/api)
# 2. [OpenWeatherMap](https://home.openweathermap.org/api_keys).

weather_spec = {
    "name": "weather",
    "description": "Get the current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city, e.g. San Francisco",
            },
            "state": {
                "type": "string",
                "description": "The state code, e.g. CA",
            },
            "country": {
                "type": "string",
                "description": "The country, e.g. USA",
            },
            "units": {
                "type": "string", 
                "enum": ["metric", "imperial"],
                "description": "Units to use when reporting weather data.",
            },
        },
        "required": ["city", "state", "country"],
    },
}

def weather(city, state, country, units="imperial"):
    api_key = os.getenv("OPEN_WEATHER_MAP_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_api_link = f"{base_url}?q={city},{state},{country}&units={units}&appid={api_key}"
    
    response = requests.get(complete_api_link)
    
    if response.status_code != 200:
        return json.dumps({"error": "Unable to fetch weather data"})
    
    data = response.json()
    
    weather_info = {
        "location": f"{city}, {state}, {country}",
        "temperature": data['main']['temp'],
        "units": 'Celsius' if units == 'metric' else 'Fahrenheit',
        "forecast": data['weather'][0]['description'],
    }
    return json.dumps(weather_info)

air_quality_spec = {
    "name": "air_quality",
    "description": "Get the current air quality",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city, e.g. San Francisco",
            },
            "state": {
                "type": "string",
                "description": "The full form state name, e.g. California",
            },
            "country": {
                "type": "string",
                "description": "The country, e.g. USA",
            },
        },
        "required": ["city", "state", "country"],
    },
}

def air_quality(city, state, country):
    api_key = os.getenv("IQAIR_KEY")
    base_url = 'http://api.airvisual.com/v2/city'
    parameters = {'city': city, 'state': state, 'country': country, 'key': api_key}
    response = requests.get(base_url, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'current' in data['data'] and 'pollution' in data['data']['current']:
            aqi = data['data']['current']['pollution']['aqius']
            air_quality_info = {
                "location": f"{city}, {state}, {country}",
                "air_quality": f"{aqi} AQI",
            }
            return json.dumps(air_quality_info)
        else:
            raise Exception("Data format is not as expected, or data not available for the requested city.")
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

functions = []
functions.append(weather_spec)
functions.append(air_quality_spec)
