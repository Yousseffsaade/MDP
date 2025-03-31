import json
from pymongo import MongoClient

# -------------------
# CONFIGURATION
# -------------------
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"
DATA_FILE = "data/final_data.json"

# -------------------
# INSÉRER LES DONNÉES
# -------------------
def insert_data():
    try:
        # Connexion à MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Lire les données fusionnées
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        if data:
            collection.insert_many(data)
            print(f"{len(data)} entrées insérées dans MongoDB.")
        else:
            print("Aucune donnée à insérer.")

        client.close()

    except Exception as e:
        print(f"Erreur insertion MongoDB : {e}")

# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    insert_data()
