from pymongo import MongoClient
import requests
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(MONGO_URI)

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

deportes_db = MongoClient(MONGO_URI)['DeportesMadrid']
polideportivos_collection = deportes_db['Polideportivos']
instalaciones_deportivas_collection = deportes_db['InstalacionesDeportivasBasicas']
piscinas_collection = deportes_db['PiscinasMunicipales']

def cargar_polideportivos():
    url = "https://datos.madrid.es/egob/catalogo/200186-0-polideportivos.json"
    response = requests.get(url)
    data = response.json().get("@graph", [])

    for centro in data:
        documento = {
            "title": limpiar_texto(centro.get("title", "Sin título")),
            "relation": limpiar_texto(centro.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible")),
            "services": limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles")),
            "latitude": centro.get("location", {}).get("latitude", None),
            "longitude": centro.get("location", {}).get("longitude", None)
        }

        polideportivos_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de Polideportivos cargados exitosamente en MongoDB")

def cargar_instalaciones_deportivas_basicas():
    url = "https://datos.madrid.es/egob/catalogo/200215-0-instalaciones-deportivas.json"
    response = requests.get(url)
    data = response.json().get("@graph", [])

    for centro in data:
        documento = {
            "title": limpiar_texto(centro.get("title", "Sin título")),
            "relation": limpiar_texto(centro.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "services": limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles")),
            "latitude": centro.get("location", {}).get("latitude", None),
            "longitude": centro.get("location", {}).get("longitude", None)
        }

        instalaciones_deportivas_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de Instalaciones Deportivas Básicas cargados exitosamente en MongoDB")

def cargar_piscinas():
    url = "https://datos.madrid.es/egob/catalogo/210227-0-piscinas-publicas.json"
    response = requests.get(url)
    data = response.json().get("@graph", [])

    for centro in data:
        documento = {
            "title": limpiar_texto(centro.get("title", "Sin título")),
            "relation": limpiar_texto(centro.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible")),
            "services": limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles")),
            "latitude": centro.get("location", {}).get("latitude", None),
            "longitude": centro.get("location", {}).get("longitude", None)
        }

        piscinas_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de Piscinas cargados exitosamente en MongoDB")

if __name__ == "__main__":
    cargar_polideportivos()
    cargar_instalaciones_deportivas_basicas()
    cargar_piscinas()
