from pymongo import MongoClient
import requests
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(MONGO_URI)
db = client['ServiciosSocialesComunitarios']
centros_mayores_collection = db['CentrosMayores']
centros_atencion_menoresfamilia_collection = db['CentrosAtencionMenoresFamilia']
centros_dia_collection = db['CentrosDia']
centros_servicios_sociales_collection = db['CentrosServiciosSociales']

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

def cargar_centros_mayores():
    url = "https://datos.madrid.es/egob/catalogo/200337-0-centros-mayores.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        title = limpiar_texto(centro.get("title", "Sin título"))
        relation = limpiar_texto(centro.get("relation", "Enlace no disponible"))
        street_address = limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible"))
        organization_desc = limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible"))
        schedule = limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible"))
        services = limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles"))
        latitude = centro.get("location", {}).get("latitude", None)
        longitude = centro.get("location", {}).get("longitude", None)

        centro_data = {
            "title": title,
            "relation": relation,
            "street_address": street_address,
            "organization_desc": organization_desc,
            "schedule": schedule,
            "services": services,
            "latitude": latitude,
            "longitude": longitude
        }

        centros_mayores_collection.update_one(
            {"title": title, "street_address": street_address},
            {"$set": centro_data},
            upsert=True
        )

    print("Datos de centros de mayores cargados exitosamente en MongoDB Atlas")

def cargar_centros_atencion_menoresfamilia():
    url = "https://datos.madrid.es/egob/catalogo/205244-0-infancia-familia-adolescentes.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        title = limpiar_texto(centro.get("title", "Sin título"))
        relation = limpiar_texto(centro.get("relation", "Enlace no disponible"))
        street_address = limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible"))
        organization_desc = limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible"))
        schedule = limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible"))
        services = limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles"))
        latitude = centro.get("location", {}).get("latitude", None)
        longitude = centro.get("location", {}).get("longitude", None)

        centro_data = {
            "title": title,
            "relation": relation,
            "street_address": street_address,
            "organization_desc": organization_desc,
            "schedule": schedule,
            "services": services,
            "latitude": latitude,
            "longitude": longitude
        }

        centros_atencion_menoresfamilia_collection.update_one(
            {"title": title, "street_address": street_address},
            {"$set": centro_data},
            upsert=True
        )

    print("Datos de centros de infancia y familia cargados exitosamente en MongoDB Atlas")

def cargar_centros_dia():
    url = "https://datos.madrid.es/egob/catalogo/200342-0-centros-dia.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        title = limpiar_texto(centro.get("title", "Sin título"))
        relation = limpiar_texto(centro.get("relation", "Enlace no disponible"))
        street_address = limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible"))
        organization_desc = limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible"))
        schedule = limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible"))
        services = limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles"))
        latitude = centro.get("location", {}).get("latitude", None)
        longitude = centro.get("location", {}).get("longitude", None)

        centro_data = {
            "title": title,
            "relation": relation,
            "street_address": street_address,
            "organization_desc": organization_desc,
            "schedule": schedule,
            "services": services,
            "latitude": latitude,
            "longitude": longitude
        }

        centros_dia_collection.update_one(
            {"title": title, "street_address": street_address},
            {"$set": centro_data},
            upsert=True
        )

    print("Datos de centros de día cargados exitosamente en MongoDB Atlas")

def cargar_centros_servicios_sociales():
    url = "https://datos.madrid.es/egob/catalogo/209094-0-centros-servicios-sociales.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        title = limpiar_texto(centro.get("title", "Sin título"))
        relation = limpiar_texto(centro.get("relation", "Enlace no disponible"))
        street_address = limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible"))
        organization_desc = limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible"))
        schedule = limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible"))
        services = limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles"))
        latitude = centro.get("location", {}).get("latitude", None)
        longitude = centro.get("location", {}).get("longitude", None)

        centro_data = {
            "title": title,
            "relation": relation,
            "street_address": street_address,
            "organization_desc": organization_desc,
            "schedule": schedule,
            "services": services,
            "latitude": latitude,
            "longitude": longitude
        }

        centros_servicios_sociales_collection.update_one(
            {"title": title, "street_address": street_address},
            {"$set": centro_data},
            upsert=True
        )

    print("Datos de centros de servicios sociales cargados exitosamente en MongoDB Atlas")

if __name__ == "__main__":
    cargar_centros_mayores()
    cargar_centros_atencion_menoresfamilia()
    cargar_centros_dia()
    cargar_centros_servicios_sociales()