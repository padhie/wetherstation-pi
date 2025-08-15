import requests

def get_weather(open_weather):
    url = f"http://api.weatherapi.com/v1/current.json?key={open_weather.apikey}&q={open_weather.city}&aqi=no"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()

    temp_c = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]

    return temp_c, humidity, condition