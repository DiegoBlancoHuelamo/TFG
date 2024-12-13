from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

actividades_bp = Blueprint('actividades', __name__, url_prefix='/actividades')

client = MongoClient(MONGO_URI)
db = client['ActividadesMadrid']
actividades_bibliotecas_collection = db['ActividadesBibliotecas']
actividades_culturales_ocio_collection = db['ActividadesCulturalesOcio']
actividades_deportivas_collection = db['ActividadesDeportivas']
actividades_eventos_collection = db['ActividadesEventos']

def obtener_actividades_paginas(collection, page, per_page=15):
    actividades = list(collection.find({}).skip((page - 1) * per_page).limit(per_page))
    return actividades

@actividades_bp.route('/')
def actividades_principal():
    return render_template('ActividadesMadrid/actividades.html')

@actividades_bp.route('/actividades-culturales-ocio')
def actividades_culturales_ocio():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()
    audience = request.args.get('audience', '').strip()
    price = request.args.get('price', '').strip()

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    if not es_busqueda_valida(search):
        search = ''
        mensaje_no_resultados = "Por favor, ingresa un término de búsqueda válido."

    filtro = {}

    if search:
        filtro['title'] = {'$regex': f"{search}", '$options': 'i'}
    else:
        mensaje_no_resultados = "No se encontraron resultados para la búsqueda actual."

    if audience == "unspecified":
        filtro['audience'] = {'$regex': 'Público no especificado', '$options': 'i'}
    elif audience == "specific":
        filtro['audience'] = {'$not': {'$regex': 'Público no especificado', '$options': 'i'}}

    if price == "free":
        filtro['price'] = {'$eq': 'Gratuito'}

    actividades = list(actividades_culturales_ocio_collection.find(filtro).skip((page - 1) * 15).limit(15))

    total_actividades = actividades_culturales_ocio_collection.count_documents(filtro)

    return render_template('ActividadesMadrid/actividades_culturales_ocio.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15, 
                           search=search,
                           audience=audience,
                           price=price,
                           mensaje_no_resultados=mensaje_no_resultados if 'mensaje_no_resultados' in locals() else '')


@actividades_bp.route('/actividades-bibliotecas')
def actividades_bibliotecas():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()
    audience = request.args.get('audience', '').strip()

    filtro = {}

    if audience == "unspecified":
        filtro['audience'] = {'$regex': 'Público no especificado', '$options': 'i'}
    elif audience == "specific":
        filtro['audience'] = {'$not': {'$regex': 'Público no especificado', '$options': 'i'}}

    actividades = list(actividades_bibliotecas_collection.find(filtro).skip((page - 1) * 15).limit(15))

    total_actividades = actividades_bibliotecas_collection.count_documents(filtro)

    return render_template('ActividadesMadrid/actividades_bibliotecas.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15, 
                           search=search,
                           audience=audience)


@actividades_bp.route('/actividades-deportivas')
def actividades_deportivas():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()
    audience = request.args.get('audience', '').strip()
    price = request.args.get('price', '').strip()

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    if not es_busqueda_valida(search):
        search = ''
        mensaje_no_resultados = "Por favor, ingresa un término de búsqueda válido."

    filtro = {}

    if search:
        filtro['title'] = {'$regex': f"^{search}", '$options': 'i'}
    else:
        mensaje_no_resultados = "No se encontraron resultados para la búsqueda actual."

    if audience == "unspecified":
        filtro['audience'] = {'$regex': 'Público no especificado', '$options': 'i'}
    elif audience == "specific":
        filtro['audience'] = {'$not': {'$regex': 'Público no especificado', '$options': 'i'}}

    if price == "free":
        filtro['price'] = {'$eq': 'Gratuito'}

    actividades = list(actividades_deportivas_collection.find(filtro).skip((page - 1) * 15).limit(15))

    total_actividades = actividades_deportivas_collection.count_documents(filtro)

    return render_template('ActividadesMadrid/actividades_deportivas.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15, 
                           search=search,
                           audience=audience,
                           price=price,
                           mensaje_no_resultados=mensaje_no_resultados if 'mensaje_no_resultados' in locals() else '')

@actividades_bp.route('/actividades-eventos')
def actividades_eventos():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()
    audience = request.args.get('audience', '').strip()
    price = request.args.get('price', '').strip()

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    if not es_busqueda_valida(search):
        search = ''
        mensaje_no_resultados = "Por favor, ingresa un término de búsqueda válido."

    filtro = {}

    if search:
        filtro['title'] = {'$regex': f"^{search}", '$options': 'i'}
    else:
        mensaje_no_resultados = "No se encontraron resultados para la búsqueda actual."

    if audience == "unspecified":
        filtro['audience'] = {'$regex': 'Público no especificado', '$options': 'i'}
    elif audience == "specific":
        filtro['audience'] = {'$not': {'$regex': 'Público no especificado', '$options': 'i'}}

    if price == "free":
        filtro['price'] = {'$eq': 'Gratuito'}

    actividades = list(actividades_eventos_collection.find(filtro).skip((page - 1) * 15).limit(15))

    total_actividades = actividades_eventos_collection.count_documents(filtro)

    return render_template('ActividadesMadrid/actividades_eventos.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15, 
                           search=search,
                           audience=audience,
                           price=price,
                           mensaje_no_resultados=mensaje_no_resultados if 'mensaje_no_resultados' in locals() else '')

@actividades_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index'))

@actividades_bp.route('/mapa-bibliotecas')
def mapa_bibliotecas():
    actividades = list(actividades_bibliotecas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "link": 1, "_id": 0}
    ))
    return render_template('ActividadesMadrid/mapa_bibliotecas.html', actividades=actividades)


@actividades_bp.route('/mapa-culturales-ocio')
def mapa_culturales_ocio():
    actividades = list(actividades_culturales_ocio_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "link": 1, "_id": 0}
    ))
    return render_template('ActividadesMadrid/mapa_culturales_ocio.html', actividades=actividades)

@actividades_bp.route('/mapa-deportivas')
def mapa_deportivas():
    actividades = list(actividades_deportivas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "link": 1, "_id": 0}
    ))
    return render_template('ActividadesMadrid/mapa_deportivas.html', actividades=actividades)

@actividades_bp.route('/mapa-eventos')
def mapa_eventos():
    actividades = list(actividades_eventos_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "link": 1, "_id": 0}
    ))
    return render_template('ActividadesMadrid/mapa_eventos.html', actividades=actividades)