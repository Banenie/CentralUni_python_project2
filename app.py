import requests
import json

from flask import Flask, request

# импортирую API_KEY из другого файла
from api_key import API_KEY


# запускаю фласк приложение
app = Flask(__name__)


# получает location_key для будущих запросов погоды
def get_location_key(lat: int, lon: int) -> str:
    req = requests.get(
        'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search',
        params={'apikey': API_KEY, 'q': f'{lat},{lon}'}
        )

    location_key = req.json()['Key']

    # сохраняет ключ, чтобы экономить запросы
    with open('location_keys.json', 'w+') as file:
        json.dump(location_key, file)
    
    return location_key


# получает температуру, влажность и скорость ветра
def get_temp_humidity_wind_speed(location_key: int | str) -> dict:
    req = requests.get(
        f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}',
        params={'apikey': API_KEY, 'details': True}
        )

    weather_data = req.json()
    
    temp = weather_data[0]['Temperature']['Metric']['Value']
    humidity = weather_data[0]['RelativeHumidity']
    wind_speed = weather_data[0]['Wind']['Speed']['Metric']['Value']
    
    return {'Temperature': temp, 'Humidity': humidity, 'WindSpeed': wind_speed}


# получает вероятность дождя
def get_rain_prob(location_key: int | str) -> dict:
    req = requests.get(
        f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}',
        params={'apikey': API_KEY, 'details': True}
    )

    rain_prob = req.json()[0]['RainProbability']

    return {'RainProbability': rain_prob}


def main():
    # location_key = get_location_key(10, 10)
    location_key = '252183'
    data = get_temp_humidity_wind_speed(location_key) | get_rain_prob(location_key)

    # сохраняем данные для экономии запросов
    with open('weather_data.json', 'w+') as file:
        json.dump(data, file)


# запуск кода
if __name__ == '__main__':
    main()
    app.run(debug=True)
