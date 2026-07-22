import os
import requests
from langchain.tools import tool

API_KEY=os.getenv("OPENWEATHER_API_KEY")
BASE_URL="https://api.openweathermap.org/data/2.5/weather"

@tool
def weather_tool(city:str)->str:
    """
    Fetch current weather from a current city

    Use this tool when user ask about current weather ,
    temperature, or conditions in a specific place.
    """

    if not city or not city.strip():
        return "Error: City name can not be empty."

    if not API_KEY:
        return "Error: Weather api key is not configered."

    params={
        "q":city.strip(),
        "appid":API_KEY,
        "units":"metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code==404:
            return f"Error: City {city} not found"

        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        desription = data['weather'][0]["description"]
        humidity = data['main']['humidity']

        return {
            f"Weather in {city.title()}: {desription}",
            f"{temp}°C, humidity {humidity}%"
        }

    except requests.exceptions.Timeout:
        return "Weather server time out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: Cloud not fetch weather data. ({e})"
    

    

    

    