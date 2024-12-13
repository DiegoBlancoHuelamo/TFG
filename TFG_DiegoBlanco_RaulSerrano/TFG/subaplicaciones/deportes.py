from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

deportes_bp = Blueprint('deportes', __name__, url_prefix='/deportes')

MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['DeportesMadrid']
instalaciones_deportivas_collection = db['InstalacionesDeportivasBasicas']
piscinas_collection = db['PiscinasMunicipales']
polideportivos_collection = db['Polideportivos']

def obtener_actividades_paginas(collection, query, page, per_page=15):
    actividades = list(collection.find(query)
                             .skip((page - 1) * per_page)
                             .limit(per_page))
    return actividades

@deportes_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index')) 

@deportes_bp.route('/')
def deportes_principal():
    return render_template('Deportes/deportes.html')

@deportes_bp.route('/instalaciones') 
def instalaciones_deportivas():
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

    instalaciones = list(
        instalaciones_deportivas_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_instalaciones = instalaciones_deportivas_collection.count_documents(query)

    return render_template(
        'Deportes/instalacionesDeportivas.html',
        instalaciones=instalaciones,
        page=page,
        total_instalaciones=total_instalaciones,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@deportes_bp.route('/instalaciones/mapa') 
def mapa_instalaciones_deportivas():
    instalaciones = list(instalaciones_deportivas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('Deportes/mapa_instalacionesDeportivas.html', instalaciones=instalaciones)

@deportes_bp.route('/piscinas') 
def piscinas():
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

    piscinas = list(
        piscinas_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_piscinas = piscinas_collection.count_documents(query)

    return render_template(
        'Deportes/piscinas.html',
        piscinas=piscinas,
        page=page,
        total_piscinas=total_piscinas,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@deportes_bp.route('/piscinas/mapa') 
def mapa_piscinas():
    piscinas = list(piscinas_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('Deportes/mapa_piscinas.html', piscinas=piscinas)