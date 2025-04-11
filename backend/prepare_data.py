import pandas as pd
from pymongo import MongoClient

# -------------------
# CONFIGURATION
# -------------------
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&appName=smart-flood-cluster"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"
OUTPUT_FILE = "data/clean_data.csv"

# -------------------
# PRÉPARER LES DONNÉES
# -------------------
def prepare_data():
    try:
        # Connexion à MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Lire toutes les données
        data = list(collection.find({}, {"_id": 0}))

        if not data:
            print("Aucune donnée trouvée dans MongoDB.")
            return

        # Convertir en DataFrame
        df = pd.json_normalize(data)

        # Vérifier les colonnes existantes
        print(f"Colonnes détectées : {list(df.columns)}")

        # Vérifier les valeurs manquantes
        print("\nValeurs manquantes :")
        print(df.isnull().sum())

        # Sauvegarder en CSV
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Données nettoyées et sauvegardées dans : {OUTPUT_FILE}")

        client.close()

    except Exception as e:
        print(f"Erreur : {e}")

# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    prepare_data()
