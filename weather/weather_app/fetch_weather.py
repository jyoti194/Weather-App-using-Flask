import os
import requests
import sqlite3
from dotenv import load_dotenv

# Load env file
load_dotenv()

# Replace with your actual OpenWeatherMap API key
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CITIES = ["London", "Paris", "New York", "Tokyo", "Delhi"]
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_KEY

weather_data = []

for city in CITIES:
    response = requests.get(URL.format(city))
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data:
            city_weather = {
                'city': city,
                'temperature': data['main'].get('temp', 'N/A'),
                'humidity': data['main'].get('humidity', 'N/A'),
                'pressure': data['main'].get('pressure', 'N/A'),
                'weather': data['weather'][0].get('description', 'N/A')
            }
            weather_data.append(city_weather)
        else:
            print(f"Missing data in response for city: {city}")
    else:
        print(f"Failed to fetch data for city: {city}. Status code: {response.status_code}")

# Store data in SQLite
conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        pressure INTEGER,
        weather TEXT
    )
''')
c.executemany("INSERT INTO weather VALUES (:city, :temperature, :humidity, :pressure, :weather)", weather_data)
conn.commit()
conn.close()
