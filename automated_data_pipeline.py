import json
import time
import schedule
from datetime import datetime
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient, BlobClient

# Configuration
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=flooding;AccountKey=HWlxZxLFIAhwIH8nfBoiYDtITlQjhuUcLzQF3i+4wE12J2eNnuXh7vdgxSi38Ds/2rI7nhCczfw6+AStbLllhw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "sensor-data"
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"
DATA_COLLECTION_INTERVAL = 2  # minutes

def fetch_latest_arduino_data():
    """Fetch only the most recently added blob data from Azure."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # List all blobs
        blobs = list(container_client.list_blobs())
        
        if not blobs:
            print("No blobs found in container")
            return []
        
        # Sort blobs by last modified time (most recent first)
        blobs.sort(key=lambda b: b.last_modified, reverse=True)
        
        # Get only the most recent blob
        latest_blob = blobs[0]
        print(f"Processing most recent blob: {latest_blob.name}, modified at {latest_blob.last_modified}")
        
        blob_client = container_client.get_blob_client(latest_blob.name)
        data = blob_client.download_blob().readall().decode('utf-8')
        
        try:
            entry = json.loads(data)
            # Structure data to match mobile app expectations
            filtered_entry = {
                "device_id": entry.get("device_id", "sensor_001"),
                "temperature": float(entry.get("temperature", 0)),
                "humidity": float(entry.get("humidity", 0)),
                "soil_moisture": float(entry.get("soil_moisture", 0)),
                "water_level": float(entry.get("water_level", 0)),
                "rainfall": float(entry.get("rainfall", 0)),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return [filtered_entry]
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error processing blob {latest_blob.name}: {str(e)}")
            return []
                
    except Exception as e:
        print(f"Azure fetch error: {str(e)}")
        return []

def check_duplicate_data(data_entry, collection):
    """Check if identical data already exists in MongoDB (excluding timestamp)"""
    if not data_entry:
        return True
    
    query = {
        "device_id": data_entry["device_id"],
        "temperature": data_entry["temperature"],
        "humidity": data_entry["humidity"],
        "soil_moisture": data_entry["soil_moisture"],
        "water_level": data_entry["water_level"],
        "rainfall": data_entry["rainfall"]
    }
    
    existing = collection.find_one(query)
    return existing is not None

def insert_to_mongodb(data):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        if data:
            # Check for duplicates before inserting
            for entry in data:
                if not check_duplicate_data(entry, collection):
                    result = collection.insert_one(entry)
                    print(f"Inserted new document with ID: {result.inserted_id}")
                    return True
                else:
                    print("Skipping duplicate data entry")
                    return False
        return False
        
    except Exception as e:
        print(f"MongoDB insert error: {str(e)}")
        return False
    finally:
        client.close()

def run_pipeline():
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Running pipeline")
    
    # Fetch and process data (only the latest)
    sensor_data = fetch_latest_arduino_data()
    if not sensor_data:
        print("No new data fetched from Azure")
        return
    
    # Insert to MongoDB (only if not a duplicate)
    if insert_to_mongodb(sensor_data):
        print("Pipeline completed successfully - New data added")
    else:
        print("Pipeline completed - No new data added")

if __name__ == "__main__":
    print("Starting automated data pipeline (latest data only)")
    
    # Run immediately
    run_pipeline()
    
    # Schedule periodic runs
    schedule.every(DATA_COLLECTION_INTERVAL).minutes.do(run_pipeline)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Pipeline stopped by user")