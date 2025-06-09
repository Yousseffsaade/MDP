import os

print("Étape 1 : Récupération des données capteurs + météo...")
os.system("python fetch_data.py")

print("Étape 2 : Insertion dans MongoDB...")
os.system("python insert_to_db.py")

print("Étape 3 : Préparation des données pour le modèle...")
os.system("python prepare_data.py")

print("Étape 4 : Entraînement du modèle...")
os.system("python train_model.py")

print("✅ Toutes les étapes ont été exécutées avec succès.")