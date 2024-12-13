import os
from flask import Flask, render_template
from subaplicaciones.actividadesMadrid import actividades_bp
from subaplicaciones.culturaEducacion import cultura_bp
from subaplicaciones.socialesComunitarios import comunitario_bp
from subaplicaciones.mercadosMercadillos import mercado_bp
from subaplicaciones.deportes import deportes_bp

app = Flask(__name__)

app.register_blueprint(actividades_bp)
app.register_blueprint(cultura_bp)
app.register_blueprint(comunitario_bp)
app.register_blueprint(mercado_bp)
app.register_blueprint(deportes_bp)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
