from pymongo import MongoClient
import requests
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['ActividadesMadrid']
actividades_culturales_ocio_collection = db['ActividadesCulturalesOcio']
actividades_bibliotecas_collection = db['ActividadesBibliotecas']
actividades_deportivas_collection = db['ActividadesDeportivas']
actividades_eventos_collection = db['ActividadesEventos']

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

def cargar_actividades_culturales_ocio():
    url = "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for evento in data:
        documento = {
            "title": limpiar_texto(evento.get("title", "Sin título")),
            "street_address": limpiar_texto(evento.get("address", {}).get("area", {}).get("street-address", "Dirección no disponible")),
            "free": evento.get("free", 0),
            "price": limpiar_texto("Gratuito" if evento.get("free", 0) == 1 else evento.get("price", "Precio no especificado")),
            "description": limpiar_texto(evento.get("description", "Sin descripción")),
            "dtstart": limpiar_texto(evento.get("dtstart", "Fecha de inicio no disponible")),
            "dtend": limpiar_texto(evento.get("dtend", "Fecha de fin no disponible")),
            "audience": limpiar_texto(evento.get("audience", "Público no especificado")),
            "organization_name": limpiar_texto(evento.get("organization", {}).get("organization-name", "Organización no disponible")),
            "link": limpiar_texto(evento.get("link", "No disponible")),
            "latitude": evento.get("location", {}).get("latitude", None),
            "longitude": evento.get("location", {}).get("longitude", None)
        }

        actividades_culturales_ocio_collection.update_one(
            {"title": documento["title"]}, 
            {"$setOnInsert": documento},  
            upsert=True
        )

    print("Datos de actividades culturales y de ocio cargados exitosamente en MongoDB Atlas")

def cargar_actividades_bibliotecas():
    url = "https://datos.madrid.es/egob/catalogo/206717-0-agenda-eventos-bibliotecas.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for evento in data:
        documento = {
            "title": limpiar_texto(evento.get("title", "Sin título")),
            "street_address": limpiar_texto(evento.get("address", {}).get("area", {}).get("street-address", "Dirección no disponible")),
            "description": limpiar_texto(evento.get("description", "Sin descripción")),
            "dtstart": limpiar_texto(evento.get("dtstart", "Fecha de inicio no disponible")),
            "dtend": limpiar_texto(evento.get("dtend", "Fecha de fin no disponible")),
            "audience": limpiar_texto(evento.get("audience", "Público no especificado")),
            "organization_name": limpiar_texto(evento.get("organization", {}).get("organization-name", "Organización no disponible")),
            "link": limpiar_texto(evento.get("link", "No disponible")),
            "event_location": limpiar_texto(evento.get("event-location", "Ubicación no disponible")),
            "latitude": evento.get("location", {}).get("latitude", None),
            "longitude": evento.get("location", {}).get("longitude", None)
        }

        actividades_bibliotecas_collection.update_one(
            {"title": documento["title"], "dtstart": documento["dtstart"]}, 
            {"$setOnInsert": documento},  
            upsert=True
        )

    print("Datos de actividades en bibliotecas municipales cargados exitosamente en MongoDB Atlas")

def cargar_actividades_deportivas():
    url = "https://datos.madrid.es/egob/catalogo/212504-0-agenda-actividades-deportes.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for evento in data:
        documento = {
            "title": limpiar_texto(evento.get("title", "Sin título")),
            "street_address": limpiar_texto(evento.get("address", {}).get("area", {}).get("street-address", "Dirección no disponible")),
            "free": evento.get("free", 0),
            "price": limpiar_texto("Gratuito" if evento.get("free", 0) == 1 else evento.get("price", "Precio no especificado").strip() or "Precio no especificado"),
            "dtstart": limpiar_texto(evento.get("dtstart", "Fecha de inicio no disponible").strip() or "Fecha de inicio no disponible"),
            "dtend": limpiar_texto(evento.get("dtend", "Fecha de fin no disponible").strip() or "Fecha de fin no disponible"),
            "audience": limpiar_texto(evento.get("audience", "Público no especificado").strip() or "Público no especificado"),
            "organization_name": limpiar_texto(evento.get("organization", {}).get("organization-name", "Organización no disponible").strip() or "Organización no disponible"),
            "link": limpiar_texto(evento.get("link", "No disponible").strip() or "No disponible"),
            "event_location": limpiar_texto(evento.get("event-location", "Ubicación no disponible").strip() or "Ubicación no disponible"),
            "recurrence": evento.get("recurrence", {}),
            "recurrence_days": limpiar_texto(evento.get("recurrence", {}).get("days", "").strip() or "No recurrente"),
            "latitude": evento.get("location", {}).get("latitude", None),
            "longitude": evento.get("location", {}).get("longitude", None)
        }

        actividades_deportivas_collection.update_one(
            {"title": documento["title"]}, 
            {"$setOnInsert": documento},  
            upsert=True
        )

    print("Datos de actividades deportivas cargados exitosamente en MongoDB Atlas")

def cargar_agenda_eventos():
    url = "https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for evento in data:
        free = evento.get("free", 0)
        documento = {
            "title": limpiar_texto(evento.get("title", "Sin título")),
            "description": limpiar_texto(evento.get("description", "Sin descripción").strip() or "Sin descripción"),
            "free": free,  
            "price": limpiar_texto("Gratuito" if free == 1 else evento.get("price", "Precio no especificado")),
            "dtstart": limpiar_texto(evento.get("dtstart", "Fecha de inicio no disponible").strip() or "Fecha de inicio no disponible"),
            "dtend": limpiar_texto(evento.get("dtend", "Fecha de fin no disponible").strip() or "Fecha de fin no disponible"),
            "audience": limpiar_texto(evento.get("audience", "Público no especificado").strip() or "Público no especificado"),
            "organization_name": limpiar_texto(evento.get("organization", {}).get("organization-name", "Organización no disponible").strip() or "Organización no disponible"),
            "link": limpiar_texto(evento.get("link", "No disponible").strip() or "No disponible"),
            "event_location": limpiar_texto(evento.get("event-location", "Ubicación no disponible").strip() or "Ubicación no disponible"),
            "recurrence": evento.get("recurrence", {}),
            "recurrence_days": limpiar_texto(evento.get("recurrence", {}).get("days", "Ninguno").strip() or "Ninguno"),
            "street_address": limpiar_texto(evento.get("address", {}).get("area", {}).get("street-address", "Dirección no disponible")),
            "latitude": evento.get("location", {}).get("latitude", None),
            "longitude": evento.get("location", {}).get("longitude", None)
        }

        actividades_eventos_collection.update_one(
            {"title": documento["title"], "dtstart": documento["dtstart"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de eventos cargados exitosamente en MongoDB Atlas")

if __name__ == "__main__":
    cargar_actividades_culturales_ocio()
    cargar_actividades_bibliotecas()
    cargar_actividades_deportivas()
    cargar_agenda_eventos()