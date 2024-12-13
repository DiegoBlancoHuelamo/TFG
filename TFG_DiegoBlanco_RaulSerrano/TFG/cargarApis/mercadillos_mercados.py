from pymongo import MongoClient
import requests
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

def cargar_mercadillos():
    url = "https://datos.madrid.es/egob/catalogo/202105-0-mercadillos.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    mercadillos_collection = client["mercados_y_mercadillos"]["mercadillos"] 

    for mercadillo in data:
        documento = {
            "title": limpiar_texto(mercadillo.get("title", "Sin título")),
            "street_address": limpiar_texto(mercadillo.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(mercadillo.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(mercadillo.get("organization", {}).get("schedule", "Horario no disponible")),
            "relation": limpiar_texto(mercadillo.get("relation", "Enlace no disponible")),
            "latitude": mercadillo.get("location", {}).get("latitude", None),
            "longitude": mercadillo.get("location", {}).get("longitude", None)
        }

        mercadillos_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de mercadillos cargados exitosamente en MongoDB")

def cargar_mercados():
    url = "https://datos.madrid.es/egob/catalogo/202105-0-mercados.json"  # Cambiar la URL por la correcta cuando esté disponible
    response = requests.get(url)
    data = response.json()["@graph"]

    mercados_collection = client["mercados_y_mercadillos"]["mercados"] 

    for mercado in data:
        documento = {
            "title": limpiar_texto(mercado.get("title", "Sin título")),
            "street_address": limpiar_texto(mercado.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(mercado.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(mercado.get("organization", {}).get("schedule", "Horario no disponible")),
            "relation": limpiar_texto(mercado.get("relation", "Enlace no disponible")),
            "latitude": mercado.get("location", {}).get("latitude", None),
            "longitude": mercado.get("location", {}).get("longitude", None)
        }

        mercados_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de mercados cargados exitosamente en MongoDB")


if __name__ == "__main__":
    cargar_mercadillos()
    cargar_mercados()
