from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

cultura_bp = Blueprint('cultura', __name__, url_prefix='/cultura')

MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['CulturaEducacionMadrid']
bibliotecas_collection = db['bibliotecas']
centros_culturales_collection = db['centros_culturales']
colegios_publicos_collection = db['colegios_publicos']
escuelas_idiomas_collection = db['escuelas_idiomas']
centros_educativos_collection = db['centros_educativos']
centros_ens_artisticas_collection = db['centros_ens_artisticas']

def obtener_actividades_paginas(collection, query, page, per_page=15):
    actividades = list(collection.find(query)
                             .skip((page - 1) * per_page)
                             .limit(per_page))
    return actividades

@cultura_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index')) 

@cultura_bp.route('/')
def cultura_principal():
    return render_template('CulturaEducacion/culturaEducacion.html')

@cultura_bp.route('/bibliotecas')
def bibliotecas():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    bibliotecas = obtener_actividades_paginas(bibliotecas_collection, query, page, per_page)
    total_bibliotecas = bibliotecas_collection.count_documents(query)

    return render_template('CulturaEducacion/bibliotecas.html', 
                           bibliotecas=bibliotecas, 
                           page=page,
                           total_bibliotecas=total_bibliotecas,
                           per_page=per_page,
                           search=search)

@cultura_bp.route('/bibliotecas/mapa')
def mapa_bibliotecas():
    bibliotecas = list(bibliotecas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))
    return render_template('CulturaEducacion/mapa_bibliotecasCultura.html', bibliotecas=bibliotecas)

@cultura_bp.route('/centros-culturales')
def centros_culturales():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '').strip()
    query = {}

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    mensaje_no_resultados = ''
    
    if not es_busqueda_valida(search):
        search = ''
    elif search:
        query['title'] = {'$regex': search, '$options': 'i'}

    centros_culturales = list(
        centros_culturales_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_centros_culturales = centros_culturales_collection.count_documents(query)

    return render_template(
        'CulturaEducacion/centrosCulturales.html',
        centros_culturales=centros_culturales,
        page=page,
        total_centros_culturales=total_centros_culturales,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@cultura_bp.route('/centros-culturales/mapa')
def mapa_centros_culturales():
    centros_culturales = list(centros_culturales_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('CulturaEducacion/mapa_centrosCulturales.html', centros_culturales=centros_culturales)

@cultura_bp.route('/escuelas-idiomas')
def escuelas_idiomas():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    escuelas_idiomas = obtener_actividades_paginas(escuelas_idiomas_collection, query, page, per_page)
    total_escuelas_idiomas = escuelas_idiomas_collection.count_documents(query)

    return render_template('CulturaEducacion/escuelasIdiomas.html', 
                           escuelas_idiomas=escuelas_idiomas, 
                           page=page,
                           total_escuelas_idiomas=total_escuelas_idiomas,
                           per_page=per_page,
                           search=search)

@cultura_bp.route('/escuelas_idiomas/mapa')
def mapa_escuelas_idiomas():
    escuelas_idiomas = list(escuelas_idiomas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))
    return render_template('CulturaEducacion/mapa_escuelasIdiomas.html', escuelas_idiomas=escuelas_idiomas)

@cultura_bp.route('/colegios-publicos')
def colegios_publicos():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '').strip()
    query = {}

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    mensaje_no_resultados = ''
    
    if not es_busqueda_valida(search):
        search = ''
        mensaje_no_resultados = "Por favor, ingresa un término de búsqueda válido."
    elif search:
        query['title'] = {'$regex': search, '$options': 'i'}

    if not mensaje_no_resultados and not query:
        mensaje_no_resultados = "No se encontraron resultados para la búsqueda actual."

    colegios_publicos = list(
        colegios_publicos_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_colegios_publicos = colegios_publicos_collection.count_documents(query)

    return render_template(
        'CulturaEducacion/colegiosPublicos.html',
        colegios_publicos=colegios_publicos,
        page=page,
        total_colegios_publicos=total_colegios_publicos,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@cultura_bp.route('/colegios-publicos/mapa')
def mapa_colegios_publicos():
    colegios_publicos = list(colegios_publicos_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('CulturaEducacion/mapa_colegiosPublicos.html', colegios_publicos=colegios_publicos)

@cultura_bp.route('/centros-educativos')
def centros_educativos():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '').strip()
    query = {}

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    mensaje_no_resultados = ''
    
    if not es_busqueda_valida(search):
        search = ''
    elif search:
        query['title'] = {'$regex': search, '$options': 'i'}

    centros_educativos = list(
        centros_educativos_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_centros_educativos = centros_educativos_collection.count_documents(query)

    return render_template(
        'CulturaEducacion/centrosEducativos.html',
        centros_educativos=centros_educativos,
        page=page,
        total_centros_educativos=total_centros_educativos,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@cultura_bp.route('/centros-educativos/mapa')
def mapa_centros_educativos():
    centros_educativos = list(centros_educativos_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1,"street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('CulturaEducacion/mapa_centrosEducativos.html', centros_educativos=centros_educativos)

@cultura_bp.route('/centros-artisticas')
def centros_artisticas():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '').strip()
    query = {}

    def es_busqueda_valida(busqueda):
        if len(busqueda) < 1 or not busqueda.isalpha():
            return False
        return True

    mensaje_no_resultados = ''
    
    if not es_busqueda_valida(search):
        search = ''
    elif search:
        query['title'] = {'$regex': search, '$options': 'i'}

    centros_artisticas = list(
        centros_ens_artisticas_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_centros_artisticas = centros_ens_artisticas_collection.count_documents(query)

    return render_template(
        'CulturaEducacion/centrosEnseñanzasArtisticas.html',
        centros_artisticas=centros_artisticas,
        page=page,
        total_centros_artisticas=total_centros_artisticas,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@cultura_bp.route('/centros-artisticas/mapa')
def mapa_centros_artisticas():
    centros_artisticas = list(centros_ens_artisticas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1,"street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('CulturaEducacion/mapa_centrosArtisticas.html', centros_artisticas=centros_artisticas)