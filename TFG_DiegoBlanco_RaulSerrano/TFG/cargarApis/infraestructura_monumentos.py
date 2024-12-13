import requests
from pymongo import MongoClient
MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["Infraestructura_Monumentos_Madrid"]
edificios_collection = db["edificios_caracter_monumental"]
papeleras_collection = db["papeleras_mascotas"]
fuentes_collection = db["fuentes_para_beber"]

def limpiar_texto(texto):
    if not texto or texto.isspace():
        return "Información no disponible"
    return " ".join(texto.strip().split())

def cargar_Edificios_Caracter_Monumental():
    url = "https://datos.madrid.es/egob/catalogo/208844-0-monumentos-edificios.json"
    response = requests.get(url)
    data = response.json()["@graph"]

    for centro in data:
        edificio = {
            "title": limpiar_texto(centro.get("title", "Sin título")),
            "relation": limpiar_texto(centro.get("relation", "Enlace no disponible")),
            "street_address": limpiar_texto(centro.get("address", {}).get("street-address", "Dirección no disponible")),
            "latitude": centro.get("location", {}).get("latitude", None),
            "longitude": centro.get("location", {}).get("longitude", None)
        }
        edificios_collection.update_one({"title": edificio["title"]}, {"$set": edificio}, upsert=True)

    print("Datos de Edificios de caracter monumental cargados exitosamente en MongoDB")

def cargar_papelerasMascotas():
    url = "https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/mint_papeleras_can.json?pageSize=100&page=1"
    papeleras_data = []
    page = 1

    while url:
        print(f"Procesando página {page}...")
        response = requests.get(url)
        data = response.json()
        
        for registro in data["records"]:
            papelera = {
                "ID": registro["ID"],
                "DESC_CLASIFICACION": limpiar_texto(registro.get("DESC_CLASIFICACION", "")),
                "BARRIO": limpiar_texto(registro.get("BARRIO", "")),
                "DISTRITO": limpiar_texto(registro.get("DISTRITO", "")),
                "ESTADO": limpiar_texto(registro.get("ESTADO", "")),
                "LATITUD": registro.get("LATITUD", None),
                "LONGITUD": registro.get("LONGITUD", None),
                "DIRECCION_AUX": limpiar_texto(registro.get("DIRECCION_AUX", "")),
                "FECHA_INSTALACION": registro.get("FECHA_INSTALACION", "Información no disponible"),
                "CODIGO_INTERNO": registro.get("CODIGO_INTERNO", ""),
                "CONTRATO_COD": registro.get("CONTRATO_COD", ""),
                "TIPO": limpiar_texto(registro.get("TIPO", "")),
                "MODELO": limpiar_texto(registro.get("MODELO", ""))
            }
            papeleras_data.append(papelera)

        url = data.get("next", None)
        page += 1

    for papelera in papeleras_data:
        papeleras_collection.update_one({"ID": papelera["ID"]}, {"$set": papelera}, upsert=True)

    print(f"Se han cargado papeleras para mascotas en MongoDB.")

def cargar_fuentes_madrid():
    url = "https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/mint_fuentes.json?pageSize=100&page=1"
    fuentes_data = []
    page = 1

    while url:
        print(f"Procesando página {page}...")
        response = requests.get(url)
        data = response.json()
        
        for registro in data["records"]:
            fuente = {
                "ID": registro["ID"],
                "DESC_CLASIFICACION": limpiar_texto(registro.get("DESC_CLASIFICACION", "")),
                "BARRIO": limpiar_texto(registro.get("BARRIO", "")),
                "DISTRITO": limpiar_texto(registro.get("DISTRITO", "")),
                "ESTADO": limpiar_texto(registro.get("ESTADO", "")),
                "LATITUD": registro.get("LATITUD", None),
                "LONGITUD": registro.get("LONGITUD", None),
                "DIRECCION_AUX": limpiar_texto(registro.get("DIRECCION_AUX", "")),
                "FECHA_INSTALACION": registro.get("FECHA_INSTALACION", "Información no disponible"),
                "CODIGO_INTERNO": registro.get("CODIGO_INTERNO", ""),
                "CONTRATO_COD": registro.get("CONTRATO_COD", ""),
                "UBICACION": limpiar_texto(registro.get("UBICACION", "")),
                "USO": limpiar_texto(registro.get("USO", "")),
                "MODELO": limpiar_texto(registro.get("MODELO", ""))
            }
            fuentes_data.append(fuente)

        url = data.get("next", None)
        page += 1

    for fuente in fuentes_data:
        fuentes_collection.update_one({"ID": fuente["ID"]}, {"$set": fuente}, upsert=True)

    print(f"Se han cargado {len(fuentes_data)} fuentes en MongoDB.")

if __name__ == "__main__":
    cargar_Edificios_Caracter_Monumental()
    cargar_papelerasMascotas()
    cargar_fuentes_madrid()