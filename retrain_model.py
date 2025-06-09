import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import pickle
from pymongo import MongoClient

# Configuration
MONGO_URI = "mongodb+srv://yousseffsaade:IUeU8fHqfwawdNGU@smart-flood-cluster.slgz5lj.mongodb.net/?retryWrites=true&w=majority&appName=smart-flood-cluster"
DB_NAME = "smart_flood_system"
COLLECTION_NAME = "sensor_data"
MODEL_FILE = "model/flood_model.pkl"
MIN_DATA_POINTS = 100

def get_training_data():
    """Fetch training data from MongoDB (newest at end of collection)"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Get document count and calculate skip position
    total_docs = collection.count_documents({})
    skip_amount = max(0, total_docs - 1000)  # Get most recent 1000 records
    
    # Query documents (newest at end)
    cursor = collection.find(
        {},
        {
            "_id": 0,
            "temperature": 1,
            "humidity": 1,
            "soil_moisture": 1,
            "water_level": 1,
            "rainfall": 1
        }
    ).skip(skip_amount)
    
    # Convert to DataFrame and reverse order
    data = list(cursor)
    data.reverse()
    df = pd.DataFrame(data)
    client.close()
    
    if len(df) < MIN_DATA_POINTS:
        print(f"Warning: Only {len(df)} records found. Using sample data.")
        return create_sample_data()
    
    return df

def create_sample_data():
    """Create sample data matching mobile app fields"""
    np.random.seed(42)
    n_samples = 500
    
    # Normal conditions
    normal_data = {
        "temperature": np.random.uniform(15, 30, int(n_samples*0.7)),
        "humidity": np.random.uniform(30, 70, int(n_samples*0.7)),
        "soil_moisture": np.random.uniform(20, 60, int(n_samples*0.7)),
        "water_level": np.random.uniform(10, 40, int(n_samples*0.7)),
        "rainfall": np.random.uniform(0, 10, int(n_samples*0.7))
    }
    
    # Flood conditions
    flood_data = {
        "temperature": np.random.uniform(10, 25, int(n_samples*0.3)),
        "humidity": np.random.uniform(70, 95, int(n_samples*0.3)),
        "soil_moisture": np.random.uniform(60, 90, int(n_samples*0.3)),
        "water_level": np.random.uniform(50, 120, int(n_samples*0.3)),
        "rainfall": np.random.uniform(20, 50, int(n_samples*0.3))
    }
    
    # Combine data
    df_normal = pd.DataFrame(normal_data)
    df_normal["flood_risk"] = 0
    
    df_flood = pd.DataFrame(flood_data)
    df_flood["flood_risk"] = 1
    
    return pd.concat([df_normal, df_flood], ignore_index=True)

def train_model():
    try:
        # Get data
        df = get_training_data()
        
        # Create target variable
        df["flood_risk"] = ((df["water_level"] >= 50) | (df["rainfall"] >= 20)).astype(int)
        
        # Features and target
        features = ["temperature", "humidity", "soil_moisture", "water_level", "rainfall"]
        X = df[features]
        y = df["flood_risk"]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight="balanced"
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        print("\nModel Evaluation:")
        y_pred = model.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        
        # Save model
        os.makedirs("model", exist_ok=True)
        with open(MODEL_FILE, "wb") as f:
            pickle.dump(model, f)
            
        print(f"\n✅ Model saved to {MODEL_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting model training...")
    if train_model():
        print("✅ Training completed successfully!")
    else:
        print("❌ Training failed!")