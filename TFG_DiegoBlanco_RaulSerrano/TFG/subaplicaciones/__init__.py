from flask import Blueprint

actividades_bp = Blueprint('actividades', __name__, url_prefix='/actividades')
cultura_bp = Blueprint('cultura', __name__, url_prefix='/cultura')
comunitario_bp = Blueprint('comunitario', __name__, url_prefix='/comunitario')
mercado_bp = Blueprint('mercado', __name__, url_prefix='/mercado')
deportes_bp = Blueprint('deportes', __name__, url_prefix='/deportes')