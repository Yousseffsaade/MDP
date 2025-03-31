import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from utils.weather_api import get_weather_data

# -------------------
# CONFIGURATION
# -------------------
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=smartfloodstorage;AccountKey=5m5PKOjDAChhpVgzF5NghECvZgNCMCJ/YSHlJPfOngdGL9ic5CVFjhIYNXDm4HYjDIhng/N4lGFL+AStc9Aoqw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "sensor-data"
DATA_FILE = "data/final_data.json"

# -------------------
# RÉCUPÉRER LES DONNÉES ARDUINO
# -------------------
def fetch_arduino_data():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        sensor_entries = []
        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob.name)
            data = blob_client.download_blob().readall().decode('utf-8')
            sensor_entries.append(json.loads(data))

        return sensor_entries

    except Exception as e:
        print(f"❌ Erreur récupération Azure : {e}")
        return []

# -------------------
# FUSIONNER AVEC WEATHER API
# -------------------
def merge_data():
    print("📥 Récupération des données Arduino...")
    arduino_data = fetch_arduino_data()
    print(f"🔢 {len(arduino_data)} fichiers trouvés dans Azure.")

    print("🌦️ Appel Weather API...")
    weather = get_weather_data()
    print(f"🌡️ Données météo récupérées : {weather}")

    merged = []
    for entry in arduino_data:
        merged_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": entry.get("device_id"),
            "water_level": entry.get("water_level"),
            "rainfall": entry.get("rainfall"),
            "soil_moisture": entry.get("soil_moisture"),
            "humidity": entry.get("humidity"),
            "temperature": entry.get("temperature"),
            "weather_forecast": weather
        }
        merged.append(merged_entry)

    # Sauvegarde locale
    with open(DATA_FILE, 'w') as f:
        json.dump(merged, f, indent=4)

    print(f"\n✅ Données fusionnées et sauvegardées dans {DATA_FILE}")

# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    merge_data()
