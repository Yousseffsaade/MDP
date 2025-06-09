from flask import Flask, jsonify, request
from pymongo import MongoClient
import pickle
import numpy as np
from bson import json_util
import json

# MongoDB Configuration
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&appName=smart-flood-cluster"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/")
def home():
    return "Smart Flood System API is running."

@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        # Query documents with newest first (sort by _id desc, which contains timestamp)
        cursor = collection.find(
            {},
            {
                "_id": 0,
                "timestamp": 1,
                "device_id": 1,
                "temperature": 1,
                "humidity": 1,
                "soil_moisture": 1,
                "water_level": 1,
                "rainfall": 1
            }
        ).sort("_id", -1).limit(10)  # Get only the 10 most recent entries
        
        # Convert to list (already sorted newest first)
        data = list(cursor)
        
        # Convert BSON to JSON
        data = json.loads(json_util.dumps(data))
        return jsonify({"data": data}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/latest", methods=["GET"])
def get_latest_data():
    try:
        # Get only the single most recent entry
        latest = collection.find_one(
            {},
            {
                "_id": 0,
                "timestamp": 1,
                "device_id": 1,
                "temperature": 1,
                "humidity": 1,
                "soil_moisture": 1,
                "water_level": 1,
                "rainfall": 1
            },
            sort=[("_id", -1)]  # Sort by _id desc (most recent first)
        )
        
        if not latest:
            return jsonify({"error": "No sensor data available"}), 404
            
        # Convert BSON to JSON
        latest_data = json.loads(json_util.dumps(latest))
        return jsonify({"data": latest_data}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        
        # Load model
        with open("model/flood_model.pkl", "rb") as f:
            model = pickle.load(f)

        # Extract values from request
        temperature = float(input_data.get("temperature", 0))
        humidity = float(input_data.get("humidity", 0))
        soil_moisture = float(input_data.get("soil_moisture", 0))
        water_level = float(input_data.get("water_level", 0))
        rainfall = float(input_data.get("rainfall", 0))
        
        # Print values for debugging
        print(f"Prediction input: temp={temperature}, humidity={humidity}, soil={soil_moisture}, water={water_level}, rain={rainfall}")
        
        # Create a features list in the exact order used during training
        features = [
            water_level,
            soil_moisture,
            humidity,
            temperature,
            rainfall
        ]

        # Make prediction
        prediction = model.predict([features])[0]
        
        print(f"Prediction result: {prediction}")
        
        return jsonify({
            "prediction": int(prediction),
            "status": "success"
        }), 200
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)