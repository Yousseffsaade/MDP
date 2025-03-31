# Smart Flood Detection System - Backend

## 📌 Description
Ce backend permet de :
- Récupérer les données des capteurs Arduino depuis **Azure Blob Storage**
- Récupérer les données météo en temps réel depuis **OpenWeather API**
- Fusionner les deux
- Sauvegarder les données fusionnées dans **MongoDB Atlas**

---

## 🚀 Prérequis

- Python 3.10+
- Git
- Compte Azure (avec Storage Account configuré)
- Compte OpenWeather (clé API)
- Compte MongoDB Atlas (Cluster Free configuré)

---

## ⚙️ Installation et exécution

### 1. Cloner le projet

git clone https://github.com/Yousseffsaade/MDP.git
cd MDP/backend

### 2. Créer l'environnement virtuel

python -m venv venv
venv\Scripts\activate

### 3. Installer les dépendances

pip install -r requirements.txt

ou

pip install azure-storage-blob pymongo requests

### 4. Configurer les paramètres

Ouvrir les fichiers suivants et remplacer les variables :

fetch_data.py
AZURE_CONNECTION_STRING
utils/weather_api.py
API_KEY
insert_to_db.py
MONGO_URI

### 5. Exécuter les scripts

A. Vérifier la connexion Azure :

python test_azure_connection.py

B. Récupérer les données Arduino + météo :

python fetch_data.py

C. Insérer les données dans MongoDB :

python insert_to_db.py

✅ Résultat attendu

Le fichier data/final_data.json sera rempli avec les données fusionnées.
Les données seront insérées dans la base MongoDB Atlas.



