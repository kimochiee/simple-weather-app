import requests
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, render_template, request


app = Flask(__name__, template_folder='./templates/')


def createChart(data):
    dates = [d['date'] for d in data]
    temperatures = [d['temp'] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, temperatures)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Trend')
    plt.savefig('static/images/weather_chart.png')


def getCurrentWeather(data):
    return {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed'],
        'currentTime': datetime.now().strftime('%H:%M'),
        'type': data['weather'][0]['main'],
        'day': datetime.now().strftime('%A')
    }


def getWeatherForecast(lat, lon, api_key):
    url2 = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    response2 = requests.get(url2)
    data2 = response2.json()
    results = []

    for item in data2["list"]:
        if item["dt_txt"].endswith("12:00:00"):
            temp = round(item["main"]["temp"] - 273.15, 2)
            date = datetime.strptime(
                item["dt_txt"], '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%y")
            type = item["weather"][0]["main"]
            icon = f'http://openweathermap.org/img/w/{item["weather"][0]["icon"]}.png'
            results.append({"temp": temp, "date": date,
                           "type": type, "icon": icon})

    return results


@app.route('/', methods=['GET', 'POST'])
def weather():
    api_key = open('env/.env', 'r').read()

    if request.method == 'POST':
        city = request.form['city']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            document = getCurrentWeather(data)
            lat = data['coord']['lat']
            lon = data['coord']['lon']

            results = getWeatherForecast(lat, lon, api_key)
            createChart(results)

            return render_template('index.html', document=document, forecast=results)
        else:
            return render_template('index.html', error='City not found')
    elif request.method == 'GET':
        city = 'saigon'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            document = getCurrentWeather(data)
            lat = data['coord']['lat']
            lon = data['coord']['lon']

            results = getWeatherForecast(lat, lon, api_key)
            createChart(results)

            return render_template('index.html', document=document, forecast=results)
        else:
            return render_template('index.html', error='City not found')


if __name__ == '__main__':
    app.run()
