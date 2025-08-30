# =====================================================================
# API DE COMODIDADES - Versión 0.1
# Este es el punto de entrada de nuestra aplicación.
# =====================================================================

from flask import Flask

# Creamos la aplicación web con Flask
app = Flask(__name__)

# Definimos una ruta de prueba para saber que está funcionando
@app.route('/')
def index():
    return "Hola, soy la amenities-api!"

# Código para que Easypanel pueda ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
