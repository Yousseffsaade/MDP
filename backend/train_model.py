import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -------------------
# CONFIGURATION
# -------------------
DATA_FILE = "data/clean_data.csv"
MODEL_FILE = "model/flood_risk_model.pkl"

# -------------------
# ENTRAÎNEMENT DU MODÈLE
# -------------------
def train_model():
    try:
        # Charger les données
        df = pd.read_csv(DATA_FILE)

        # Créer une étiquette binaire : 1 si water_level >= 50cm ou rainfall > 20mm
        df["flood_risk"] = ((df["water_level"] >= 50) | (df["rainfall"] > 20)).astype(int)

        # Sélectionner les colonnes utiles
        features = [
            "water_level", "soil_moisture", "humidity", "temperature",
            "weather_forecast.forecast_temperature",
            "weather_forecast.forecast_humidity",
            "weather_forecast.predicted_rain",
            "weather_forecast.wind_speed"
        ]
        X = df[features]
        y = df["flood_risk"]

        # Séparer en train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Créer et entraîner le modèle
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Évaluer le modèle
        y_pred = model.predict(X_test)
        print("\nÉvaluation du modèle :")
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        # Sauvegarder le modèle
        joblib.dump(model, MODEL_FILE)
        print(f"\n✅ Modèle entraîné et sauvegardé dans : {MODEL_FILE}")

    except Exception as e:
        print(f"Erreur : {e}")

# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    train_model()
