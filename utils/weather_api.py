import requests

# Remplace par ta clé API Weather
API_KEY = "3cb62b6d97b43ff448eefd08e762e674"
LAT = "33.89"  # Exemple : Beyrouth
LON = "35.50"

def get_weather_data():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather_info = {
            "forecast_temperature": data["main"]["temp"],
            "forecast_humidity": data["main"]["humidity"],
            "predicted_rain": data.get("rain", {}).get("1h", 0),
            "wind_speed": data["wind"]["speed"]
        }
        return weather_info

    except Exception as e:
        print(f"Erreur récupération météo : {e}")
        return {}
