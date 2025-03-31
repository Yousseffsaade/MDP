✅ Résumé de l’avancement du projet

1. Configuration du stockage Cloud Azure

Création d’un Storage Account Azure (smartfloodstorage).
Création d’un Container Blob nommé sensor-data pour stocker les données venant de l'Arduino.
Téléversement d’un fichier de test JSON contenant des données Arduino simulées.
2. Création d’une API Weather externe

Ajout de l'utilisation de l'API OpenWeather dans le projet.
Intégration dans le fichier fetch_data.py pour récupérer :
Température
Humidité
Prévision de pluie
Vitesse du vent
3. Récupération et fusion des données

Développement du script Python fetch_data.py qui fait :
Récupération des fichiers stockés sur Azure Blob Storage.
Appel à l'API météo.
Fusion des données météo et des données Arduino.
Sauvegarde de ces données fusionnées dans un fichier local data/final_data.json.
4. Création et configuration de la base de données

Création d’un Cluster MongoDB Atlas (gratuit, sandbox).
Création de la base de données : smart_flood_system.
Création de la collection : sensor_data.
Connexion sécurisée avec un utilisateur MongoDB et whitelist de l’adresse IP.
5. Insertion des données dans MongoDB

Développement du script Python insert_to_db.py qui :
Se connecte à MongoDB.
Charge les données fusionnées depuis data/final_data.json.
Insère les données dans la collection sensor_data.
Résultat : ✅ Données insérées avec succès (vérifié depuis MongoDB Atlas).
6. Mise en place d’une API Backend avec Flask

Création du fichier app.py.
Développement d’une API REST simple :
Endpoint : /api/data
Fonction : Lire les données depuis MongoDB et les afficher en format JSON.
Test de l’API en local : ✅ Affichage des données sur http://127.0.0.1:5000/api/data
🚀 Avancement global

Partie	Statut
Stockage Cloud (Azure Blob)	✅ Fait
API météo (OpenWeather)	✅ Intégrée
Récupération & Fusion données	✅ Fait
Base de données (MongoDB)	✅ Configurée & connectée
Insertion des données	✅ Fonctionnel
API Backend (Flask)	✅ Fonctionnelle
🎯 Prochaines étapes possibles

Si tu veux avancer :

Ajouter un modèle Machine Learning qui utilise ces données.
Créer une interface Mobile ou Web qui récupère les données via ton API Flask.
Implémenter un système d’alerte (email, notification) en cas de risque de flood détecté.
