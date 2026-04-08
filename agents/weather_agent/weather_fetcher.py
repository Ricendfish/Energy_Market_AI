import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city="Copenhagen"):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    r = requests.get(url)
    data = r.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    return weather


if __name__ == "__main__":
    print(get_weather())