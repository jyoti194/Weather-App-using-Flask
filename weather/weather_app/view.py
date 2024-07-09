from flask import request, jsonify, render_template
# from app import app, db
from weather_app.models import Weather
from weather_app import app, db

@app.route('/')
def index():
    weather_data = Weather.query.all()
    return render_template('index.html', weather_data=weather_data)

@app.route('/api/weather', methods=['GET', 'POST'])
def manage_weather():
    if request.method == 'POST':
        data = request.json
        new_weather = Weather(
            city=data['city'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            weather=data['weather']
        )
        db.session.add(new_weather)
        db.session.commit()
        return jsonify({"message": "Weather data added"}), 201

    weather_data = Weather.query.all()
    return jsonify([{
        'city': w.city,
        'temperature': w.temperature,
        'humidity': w.humidity,
        'pressure': w.pressure,
        'weather': w.weather
    } for w in weather_data])

@app.route('/api/weather/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_weather(id):
    weather = Weather.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.json
        weather.city = data.get('city', weather.city)
        weather.temperature = data.get('temperature', weather.temperature)
        weather.humidity = data.get('humidity', weather.humidity)
        weather.pressure = data.get('pressure', weather.pressure)
        weather.weather = data.get('weather', weather.weather)
        
        db.session.commit()
        return jsonify({"message": "Weather data updated"})
    
    if request.method == 'DELETE':
        db.session.delete(weather)
        db.session.commit()
        return jsonify({"message": "Weather data deleted"})
