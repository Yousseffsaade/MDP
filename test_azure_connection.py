from azure.storage.blob import BlobServiceClient

# -------------------
# CONFIGURATION
# -------------------
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=smartfloodstorage;AccountKey=5m5PKOjDAChhpVgzF5NghECvZgNCMCJ/YSHlJPfOngdGL9ic5CVFjhIYNXDm4HYjDIhng/N4lGFL+AStc9Aoqw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "sensor-data"

# -------------------
# TEST DE CONNEXION
# -------------------
def list_blobs():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        print(f"Conteneur trouvé : {CONTAINER_NAME}")
        print("Liste des fichiers :")
        blobs = container_client.list_blobs()
        for blob in blobs:
            print(f" - {blob.name}")

        print("\n✅ Connexion réussie.")

    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    list_blobs()
