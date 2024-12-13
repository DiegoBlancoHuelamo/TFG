from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

comunitario_bp = Blueprint('comunitario', __name__, url_prefix='/comunitario')

MONGO_URI = "mongodb+srv://TFGDiegoRaul:ZXdY41ybUtoJ9Ada@cluster0.pemmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['ServiciosSocialesComunitarios']
centros_atencion_menores_familia_collection = db['CentrosAtencionMenoresFamilia']
centros_dia_collection = db['CentrosDia']
centros_mayores_collection = db['CentrosMayores']
centros_servicios_sociales_collection = db['CentrosServiciosSociales']


def obtener_actividades_paginas(collection, query, page, per_page=15):
    actividades = list(collection.find(query)
                             .skip((page - 1) * per_page)
                             .limit(per_page))
    return actividades

@comunitario_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index')) 

@comunitario_bp.route('/')
def comunitario_principal():
    return render_template('SocialesComunitarios/socialesComunitarios.html')


@comunitario_bp.route('/centros-familia')
def centros_familia():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    centros_familia = obtener_actividades_paginas(centros_atencion_menores_familia_collection, query, page, per_page)
    total_centros_familia = centros_atencion_menores_familia_collection.count_documents(query)

    return render_template('SocialesComunitarios/centros_familia.html', 
                           centros_familia=centros_familia, 
                           page=page,
                           total_centros_familia=total_centros_familia,
                           per_page=per_page,
                           search=search)

@comunitario_bp.route('/centros-familia/mapa')
def mapa_centros_familia():
    centros_familia = list(centros_atencion_menores_familia_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "relation": 1, "street_address": 1, "_id": 0}
    ))
    return render_template('SocialesComunitarios/mapa_centros_familia.html', centros_familia=centros_familia)

@comunitario_bp.route('/centros-dia')
def centros_dia():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    centros_dia = obtener_actividades_paginas(centros_dia_collection, query, page, per_page)
    total_centros_dia = centros_dia_collection.count_documents(query)

    return render_template('SocialesComunitarios/centros_dia.html', 
                           centros_dia=centros_dia, 
                           page=page,
                           total_centros_dia=total_centros_dia,
                           per_page=per_page,
                           search=search)

@comunitario_bp.route('/centros-dia/mapa')
def mapa_centros_dia():
    centros_dia = list(centros_dia_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "relation": 1, "street_address": 1, "_id": 0}
    ))
    return render_template('SocialesComunitarios/mapa_centros_dia.html', centros_dia=centros_dia)

@comunitario_bp.route('/centros-mayores')
def centros_mayores():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    centros_mayores = obtener_actividades_paginas(centros_mayores_collection, query, page, per_page)
    total_centros_mayores = centros_mayores_collection.count_documents(query)

    return render_template('SocialesComunitarios/centros_mayores.html', 
                           centros_mayores=centros_mayores, 
                           page=page,
                           total_centros_mayores=total_centros_mayores,
                           per_page=per_page,
                           search=search)

@comunitario_bp.route('/centros-mayores/mapa')
def mapa_centros_mayores():
    centros_mayores = list(centros_mayores_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "relation": 1, "street_address": 1, "_id": 0}
    ))
    return render_template('SocialesComunitarios/mapa_centros_mayores.html', centros_mayores=centros_mayores)

@comunitario_bp.route('/centros-sociales')
def centros_sociales():
    page = int(request.args.get('page', 1))
    per_page = 15
    search = request.args.get('search', '')
    query = {}
    if search:
        query = {'title': {'$regex': search, '$options': 'i'}}
    centros_sociales = obtener_actividades_paginas(centros_servicios_sociales_collection, query, page, per_page)
    total_centros_sociales = centros_servicios_sociales_collection.count_documents(query)

    return render_template('SocialesComunitarios/centros_servicios_sociales.html', 
                           centros_sociales=centros_sociales, 
                           page=page,
                           total_centros_sociales=total_centros_sociales,
                           per_page=per_page,
                           search=search)

@comunitario_bp.route('/centros-sociales/mapa')
def mapa_centros_sociales():
    centros_sociales = list(centros_servicios_sociales_collection.find(
        {"latitude": {"$exists": True}, "longitude": {"$exists": True}},
        {"title": 1, "latitude": 1, "longitude": 1, "relation": 1, "street_address": 1, "_id": 0}
    ))
    return render_template('SocialesComunitarios/mapa_centros_servicios_sociales.html', centros_sociales=centros_sociales)
