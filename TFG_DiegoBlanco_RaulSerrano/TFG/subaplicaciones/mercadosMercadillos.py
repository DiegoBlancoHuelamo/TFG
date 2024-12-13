from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

mercado_bp = Blueprint('mercado', __name__, url_prefix='/mercado')

MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['mercados_y_mercadillos']
mercados_collection = db['mercados']
mercadillos_collection = db['mercadillos']

def obtener_actividades_paginas(collection, query, page, per_page=15):
    actividades = list(collection.find(query)
                             .skip((page - 1) * per_page)
                             .limit(per_page))
    return actividades

@mercado_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index')) 

@mercado_bp.route('/')
def mercado_principal():
    return render_template('MercadosMercadillos/mercadosMercadillos.html')

@mercado_bp.route('/mercados') 
def mercados():
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

    mercados = list(
        mercados_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_mercados = mercados_collection.count_documents(query)

    return render_template(
        'MercadosMercadillos/mercados.html',
        mercados=mercados,
        page=page,
        total_mercados=total_mercados,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@mercado_bp.route('/mercados/mapa') 
def mapa_mercados():
    mercados = list(mercados_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('MercadosMercadillos/mapa_mercados.html', mercados=mercados)

@mercado_bp.route('/mercadillos') 
def mercadillos():
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

    mercadillos = list(
        mercadillos_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    )
    total_mercadillos = mercadillos_collection.count_documents(query)

    return render_template(
        'MercadosMercadillos/mercadillos.html',
        mercadillos=mercadillos,
        page=page,
        total_mercadillos=total_mercadillos,
        per_page=per_page,
        search=search,
        mensaje_no_resultados=mensaje_no_resultados
    )

@mercado_bp.route('/mercadillos/mapa') 
def mapa_mercadillos():
    mercadillos = list(mercadillos_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "street_address": 1, "relation": 1, "_id": 0}
    ))

    return render_template('MercadosMercadillos/mapa_mercadillos.html', mercadillos=mercadillos)