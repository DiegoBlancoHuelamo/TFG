from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from cargarApis.config import MONGO_URI
from datetime import datetime

# Crear el Blueprint para las actividades
actividades_bp = Blueprint('actividades', __name__, url_prefix='/actividades')

# Conectar con MongoDB
client = MongoClient(MONGO_URI)
db = client['ActividadesMadrid']
actividades_bibliotecas_collection = db['ActividadesBibliotecas']
actividades_culturales_ocio_collection = db['ActividadesCulturalesOcio']
actividades_deportivas_collection = db['ActividadesDeportivas']
actividades_eventos_collection = db['ActividadesEventos']

# Función para obtener actividades con paginación
def obtener_actividades_paginas(collection, page, per_page=15):
    actividades = list(collection.find({})
                             .skip((page - 1) * per_page)
                             .limit(per_page))
    return actividades

# Ruta principal de actividades
@actividades_bp.route('/')
def actividades_principal():
    return render_template('ActividadesMadrid/actividades.html')

# Ruta para actividades culturales y de ocio
@actividades_bp.route('/actividades-culturales-ocio')
def actividades_culturales_ocio():
    page = int(request.args.get('page', 1))
    actividades = obtener_actividades_paginas(actividades_culturales_ocio_collection, page)
    
    # Contar el total de actividades para calcular el número total de páginas
    total_actividades = actividades_culturales_ocio_collection.count_documents({})
    return render_template('ActividadesMadrid/actividades_culturales_ocio.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15)

@actividades_bp.route('/actividades-bibliotecas')
def actividades_bibliotecas():

    # Obtener el número de página desde la URL
    page = int(request.args.get('page', 1))
    
    # Obtener los términos de búsqueda desde los parámetros de la URL
    search = request.args.get('search', '').strip()
    audience = request.args.get('audience', '').strip()

    # Función para comprobar si la búsqueda tiene sentido
    def es_busqueda_valida(busqueda):
        if len(busqueda) < 2 or not busqueda.isalpha():
            return False
        return True
    
    # Si la búsqueda no es válida, mostramos todos los resultados
    if not es_busqueda_valida(search):
        search = ''
        mensaje_no_resultados = "Por favor, ingresa un término de búsqueda válido."

    # Crear el filtro de búsqueda
    filtro = {}
    
    if search:
        filtro['title'] = {'$regex': search, '$options': 'i'}
    else:
        mensaje_no_resultados = "No se encontraron resultados para la búsqueda actual."

    # Filtrar por público
    if audience == "unspecified":
        filtro['audience'] = {'$regex': 'Público no especificado', '$options': 'i'}
    elif audience == "specific":
        filtro['audience'] = {'$not': {'$regex': 'Público no especificado', '$options': 'i'}}

    # Filtrar las actividades según los criterios establecidos
    actividades = list(actividades_bibliotecas_collection.find(filtro)
                           .skip((page - 1) * 15)
                           .limit(15))

    # Fecha y hora actual
    ahora = datetime.now()

    # Filtrar actividades cuya fecha de fin ya ha pasado
    for actividad in actividades:
        if 'dtend' in actividad:
            try:
                # Convertir 'dtend' a objeto datetime
                fecha_fin = datetime.strptime(actividad['dtend'], '%Y-%m-%d %H:%M:%S.%f')
                # Verificar si la fecha de fin ha pasado
                actividad['expirada'] = fecha_fin < ahora
            except ValueError:
                # Manejar formatos de fecha no válidos o faltantes
                actividad['expirada'] = True  # Asumimos que está expirada si la fecha no es válida

    # Contar el total de actividades para calcular el número total de páginas
    total_actividades = actividades_bibliotecas_collection.count_documents(filtro)

    return render_template('ActividadesMadrid/actividades_bibliotecas.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15, 
                           search=search,
                           audience=audience,
                           mensaje_no_resultados=mensaje_no_resultados if 'mensaje_no_resultados' in locals() else '')

# Ruta para actividades deportivas
@actividades_bp.route('/actividades-deportivas')
def actividades_deportivas():
    page = int(request.args.get('page', 1))
    actividades = obtener_actividades_paginas(actividades_deportivas_collection, page)
    
    # Contar el total de actividades para calcular el número total de páginas
    total_actividades = actividades_deportivas_collection.count_documents({})
    return render_template('ActividadesMadrid/actividades_deportivas.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15)

# Ruta para actividades de eventos
@actividades_bp.route('/actividades-eventos')
def actividades_eventos():
    page = int(request.args.get('page', 1))
    actividades = obtener_actividades_paginas(actividades_eventos_collection, page)
    
    # Contar el total de actividades para calcular el número total de páginas
    total_actividades = actividades_eventos_collection.count_documents({})
    return render_template('ActividadesMadrid/actividades_eventos.html', 
                           actividades=actividades, 
                           total_actividades=total_actividades, 
                           page=page, 
                           per_page=15)

# Ruta para volver al inicio (index)
@actividades_bp.route('/volver-a-inicio')
def volver_a_inicio():
    return redirect(url_for('index'))  # Redirige a la página principal del sitio

# Ruta para mapa de bibliotecas
@actividades_bp.route('/mapa/bibliotecas')
def mapa_bibliotecas():
    # Obtiene las actividades con ubicaciones
    actividades = actividades_bibliotecas_collection.find({}).limit(100)
    eventos = []
    
    for actividad in actividades:
        if 'latitude' in actividad and 'longitude' in actividad:
            evento = {
                'title': actividad.get('title'),
                'latitude': actividad.get('latitude'),
                'longitude': actividad.get('longitude'),
                'event_location': actividad.get('event_location'),
                'link': actividad.get('link')
            }
            eventos.append(evento)
    
    try:
        return render_template('ActividadesMadrid/mapa_bibliotecas.html', eventos=eventos)
    except Exception as e:
        print(f"Error al cargar la plantilla: {e}")
        return "Error al cargar la plantilla"

# Ruta para mapa de actividades culturales y de ocio
@actividades_bp.route('/mapa/culturales-ocio')
def mapa_culturales_ocio():
    actividades = actividades_culturales_ocio_collection.find({}).limit(100)
    eventos = []

    for actividad in actividades:
        if 'latitude' in actividad and 'longitude' in actividad:
            evento = {
                'title': actividad.get('title'),
                'latitude': actividad.get('latitude'),
                'longitude': actividad.get('longitude'),
                'event_location': actividad.get('event_location'),
                'link': actividad.get('link')
            }
            eventos.append(evento)

    try:
        return render_template('ActividadesMadrid/mapa_culturales_ocio.html', eventos=eventos)
    except Exception as e:
        print(f"Error al cargar la plantilla: {e}")
        return "Error al cargar la plantilla"

# Ruta para mapa de actividades deportivas
@actividades_bp.route('/mapa/deportivas')
def mapa_deportivas():
    actividades = actividades_deportivas_collection.find({}).limit(100)
    eventos = []

    for actividad in actividades:
        if 'latitude' in actividad and 'longitude' in actividad:
            evento = {
                'title': actividad.get('title'),
                'latitude': actividad.get('latitude'),
                'longitude': actividad.get('longitude'),
                'event_location': actividad.get('event_location'),
                'link': actividad.get('link')
            }
            eventos.append(evento)

    try:
        return render_template('ActividadesMadrid/mapa_deportivas.html', eventos=eventos)
    except Exception as e:
        print(f"Error al cargar la plantilla: {e}")
        return "Error al cargar la plantilla"
    

@actividades_bp.route('/mapa/eventos')
def mapa_eventos():
    actividades = actividades_eventos_collection.find({}).limit(100)
    eventos = []

    for actividad in actividades:
        if 'latitude' in actividad and 'longitude' in actividad:
            evento = {
                'title': actividad.get('title'),
                'latitude': actividad.get('latitude'),
                'longitude': actividad.get('longitude'),
                'event_location': actividad.get('event_location'),
                'link': actividad.get('link')
            }
            eventos.append(evento)

    try:
        return render_template('ActividadesMadrid/mapa_eventos.html', eventos=eventos)
    except Exception as e:
        print(f"Error al cargar la plantilla: {e}")
        return "Error al cargar la plantilla"
