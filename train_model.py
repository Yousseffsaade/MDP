import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Configuration
DATA_FILE = "data/clean_data.csv"
MODEL_FILE = "model/flood_model.pkl"  # Changed to match app.py

def train_model():
    try:
        # Load data
        df = pd.read_csv(DATA_FILE)

        # Create binary label: 1 if water_level >= 50cm or rainfall > 20mm
        df["flood_risk"] = ((df["water_level"] >= 50) | (df["rainfall"] > 20)).astype(int)

        # Use only available sensor features (must match prediction order)
        features = [
            "water_level",
            "soil_moisture", 
            "humidity",
            "temperature",
            "rainfall"
        ]
        X = df[features]
        y = df["flood_risk"]

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        print("\nModel Evaluation:")
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        # Save model
        joblib.dump(model, MODEL_FILE)
        print(f"\nModel trained and saved to: {MODEL_FILE}")
        print(f"Model features: {features}")  # Important for debugging

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    train_model()