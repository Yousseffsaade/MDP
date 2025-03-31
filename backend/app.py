from flask import Flask, jsonify
from pymongo import MongoClient

# Configuration MongoDB
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&appName=smart-flood-cluster"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"

app = Flask(__name__)

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        data = list(collection.find({}, {"_id": 0}))  # Retirer l'id
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Smart Flood System API is running."

if __name__ == "__main__":
    app.run(debug=True)
