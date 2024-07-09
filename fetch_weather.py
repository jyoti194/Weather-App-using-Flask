import requests
import sqlite3

# Replace with your actual OpenWeatherMap API key
API_KEY = '7587a0e856f44270a904e68b101900e4'
CITIES = [
    {"city": "London", "state": "England", "country": "UK"},
    {"city": "Paris", "state": "Île-de-France", "country": "France"},
    {"city": "New York", "state": "NY", "country": "USA"},
    {"city": "Tokyo", "state": "Tokyo", "country": "Japan"},
    {"city": "Delhi", "state": "Delhi", "country": "India"}
]
URL = "http://api.openweathermap.org/data/2.5/weather?q={},{}&appid=" + API_KEY

weather_data = []

for location in CITIES:
    city_state_country = f"{location['city']},{location['country']}"
    response = requests.get(URL.format(location['city'], location['country']))
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data and 'wind' in data:
            city_weather = {
                'city': city_state_country,
                'temperature': data['main'].get('temp', 'N/A'),
                'humidity': data['main'].get('humidity', 'N/A'),
                'pressure': data['main'].get('pressure', 'N/A'),
                'weather': data['weather'][0].get('description', 'N/A'),
                'wind': data['wind'].get('speed', 'N/A')
            }
            weather_data.append(city_weather)
        else:
            print(f"Missing data in response for location: {city_state_country}")
    else:
        print(f"Failed to fetch data for location: {city_state_country}. Status code: {response.status_code}")

# Store data in SQLite
conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        pressure INTEGER,
        weather TEXT,
        wind REAL
    )
''')
c.executemany("INSERT INTO weather VALUES (:city, :temperature, :humidity, :pressure, :weather, :wind)", weather_data)
conn.commit()
conn.close()
