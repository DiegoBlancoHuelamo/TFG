from pymongo import MongoClient
import requests
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

client = MongoClient(MONGO_URI)
db = client['CulturaEducacionMadrid']
bibliotecas_collection = db['bibliotecas']
centros_culturales_collection = db['centros_culturales']
colegios_publicos_collection = db['colegios_publicos']
escuelas_idiomas_collection = db['escuelas_idiomas']
centros_educativos_collection = db['centros_educativos']
centros_ens_artisticas_collection = db['centros_ens_artisticas']

def cargar_bibliotecas():
    url = "https://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for biblioteca in data:
        documento = {
            "title": limpiar_texto(biblioteca.get("title", "Sin título")),
            "street_address": limpiar_texto(biblioteca.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(biblioteca.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(biblioteca.get("organization", {}).get("schedule", "Horario no disponible")),
            "services": limpiar_texto(biblioteca.get("organization", {}).get("services", "Servicios no disponibles")),
            "latitude": biblioteca.get("location", {}).get("latitude", None),
            "longitude": biblioteca.get("location", {}).get("longitude", None)
        }

        bibliotecas_collection.update_one(
            {"title": documento["title"]}, 
            {"$setOnInsert": documento}, 
            upsert=True
        )

    print("Datos de bibliotecas cargados exitosamente en MongoDB")

def cargar_centros_culturales():
    url = "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        documento = {
            "title": limpiar_texto(centro.get("title", "Sin título")),
            "street_address": limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(centro.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "schedule": limpiar_texto(centro.get("organization", {}).get("schedule", "Horario no disponible")),
            "services": limpiar_texto(centro.get("organization", {}).get("services", "Servicios no disponibles")),
            "relation": limpiar_texto(centro.get("relation", "Enlace no disponible")),
            "latitude": centro.get("location", {}).get("latitude", None),
            "longitude": centro.get("location", {}).get("longitude", None)
        }

        centros_culturales_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de centros culturales cargados exitosamente en MongoDB")

def cargar_colegios_publicos():
    url = "https://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for colegio in data:
        documento = {
            "title": limpiar_texto(colegio.get("title", "Sin título")),
            "relation": limpiar_texto(colegio.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(colegio.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(colegio.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "services": limpiar_texto(colegio.get("organization", {}).get("services", "Servicios no disponibles")),
            "latitude": colegio.get("location", {}).get("latitude", None),
            "longitude": colegio.get("location", {}).get("longitude", None)
        }

        colegios_publicos_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de colegios públicos cargados exitosamente en MongoDB")

def cargar_escuelas_idiomas():
    url = "https://datos.madrid.es/egob/catalogo/207037-0-idiomas-oficial.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for escuela in data:
        documento = {
            "title": limpiar_texto(escuela.get("title", "Sin título")),
            "relation": limpiar_texto(escuela.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(escuela.get("address", {}).get("street-address", "Dirección no disponible")),
            "organization_desc": limpiar_texto(escuela.get("organization", {}).get("organization-desc", "Descripción no disponible")),
            "latitude": escuela.get("location", {}).get("latitude", None),
            "longitude": escuela.get("location", {}).get("longitude", None)
        }

        escuelas_idiomas_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de escuelas de idiomas cargados exitosamente en MongoDB")

def cargar_centros_educativos():
    url = "https://datos.madrid.es/egob/catalogo/300614-0-centros-educativos.json"
    response = requests.get(url)
    data = response.json()["@graph"]

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

        centros_educativos_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de centros educativos cargados exitosamente en MongoDB")

def cargar_centros_ens_artisticas():
    url = "https://datos.madrid.es/egob/catalogo/203868-0-ceramica-danza-musica-dramatico.json"
    response = requests.get(url)
    data = response.json()["@graph"]

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

        centros_ens_artisticas_collection.update_one(
            {"title": documento["title"]},
            {"$setOnInsert": documento},
            upsert=True
        )

    print("Datos de Centros de Enseñanzas Artísticas cargados exitosamente en MongoDB")

if __name__ == "__main__":
    cargar_bibliotecas()
    cargar_centros_culturales()
    cargar_colegios_publicos()
    cargar_escuelas_idiomas()
    cargar_centros_educativos()
    cargar_centros_ens_artisticas()