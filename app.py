
from flask import Flask, request, jsonify, render_template
import sqlite3
import requests

application = Flask(__name__)

API_KEY = '7587a0e856f44270a904e68b101900e4'
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_KEY

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('weather.db')
    except sqlite3.error as e:
        print(e)
    return conn

def convert_units(weather_data):
    weather_data['temperature'] = round(weather_data['temperature'] - 273.15, 2)  # Kelvin to Celsius
    weather_data['pressure'] = round(weather_data['pressure'] * 0.02953, 2)  # hPa to inHg
    return weather_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    try:
        data = request.get_json()
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')

        location = f"{city},{country}"
        response = requests.get(URL.format(location))
        
        if response.status_code == 200:
            weather_data = response.json()
            if 'main' in weather_data and 'weather' in weather_data and 'wind' in weather_data:
                city_weather = {
                    'city': location,
                    'temperature': weather_data['main'].get('temp', 'N/A'),
                    'humidity': weather_data['main'].get('humidity', 'N/A'),
                    'pressure': weather_data['main'].get('pressure', 'N/A'),
                    'weather': weather_data['weather'][0].get('description', 'N/A'),
                    'wind': weather_data['wind'].get('speed', 'N/A')
                }
                city_weather = convert_units(city_weather)
                
                conn = db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO weather (city, temperature, humidity, pressure, weather, wind) VALUES (?, ?, ?, ?, ?, ?)",
                               (city_weather['city'], city_weather['temperature'], city_weather['humidity'], city_weather['pressure'], city_weather['weather'], city_weather['wind']))
                conn.commit()
                return jsonify(city_weather), 201
            else:
                return jsonify({"error": "Incomplete weather data received"}), 500
        else:
            error_message = response.json().get('message', 'Unknown error')
            return jsonify({"error": f"Failed to fetch data for location: {location}. Status code: {response.status_code}. Message: {error_message}"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@app.route('/weather/<string:city>', methods=['GET', 'PUT', 'DELETE'])
def single_weather(city):
    conn = db_connection()
    cursor = conn.cursor()
    weather = None
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM weather WHERE city LIKE ?", (f"%{city}%",))
        rows = cursor.fetchall()
        for r in rows:
            weather = {
                'city': r[0],
                'temperature': r[1],
                'humidity': r[2],
                'pressure': r[3],
                'weather': r[4],
                'wind': r[5]
            }
        if weather:
            return jsonify(weather), 200
        else:
            return jsonify({"error": "City not found"}), 404

    if request.method == 'PUT':
        sql = """UPDATE weather
                 SET temperature=?,
                     humidity=?,
                     pressure=?,
                     weather=?
                 WHERE city LIKE ?"""
        updated_weather = request.get_json()
        updated_weather = convert_units(updated_weather)
        conn.execute(sql, (updated_weather["temperature"], updated_weather["humidity"], updated_weather["pressure"], updated_weather["weather"], f"%{city}%"))
        conn.commit()
        return f"Weather data for {city} updated successfully!", 200

    if request.method == 'DELETE':
        sql = """ DELETE FROM weather WHERE city LIKE ? """
        conn.execute(sql, (f"%{city}%",))
        conn.commit()
        return f"Weather data for {city} deleted successfully!", 200

if __name__ == "__main__":
    app.run(debug=True)
