# =====================================================================
# API DE COMODIDADES - Versión 1.0
# Este archivo crea un servidor web (API) con una única función:
# buscar y devolver las comodidades de un apartamento específico.
# =====================================================================

import os
import psycopg2
from flask import Flask, jsonify

# --- PASO 1: CONFIGURACIÓN ---

# Creamos la aplicación web con Flask
app = Flask(__name__)

# Función para conectarse a la base de datos de PostgreSQL
# Usará las "variables de entorno" que configuramos en Easypanel
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS')
    )
    return conn

# --- PASO 2: LA HABILIDAD PRINCIPAL DE LA API ---

# Definimos la "ruta" o "endpoint".
# Cuando se visite la URL/properties/1/amenities, se buscarán las comodidades del apartamento con ID 1.
@app.route('/properties/<int:property_id>/amenities', methods=['GET'])
def get_property_amenities(property_id):
    try:
        # 1. Conectarse a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # 2. Construir la consulta SQL para encontrar las comodidades
        # Une las tablas 'amenities' y 'property_amenities' para obtener los nombres
        sql_query = """
            SELECT a.name
            FROM amenities a
            JOIN property_amenities pa ON a.id = pa.amenity_id
            WHERE pa.property_id = %s;
        """

        # 3. Ejecutar la consulta de forma segura
        cur.execute(sql_query, (property_id,))
        
        # 4. Obtener todos los resultados
        amenities_tuples = cur.fetchall()

        # 5. Cerrar la conexión
        cur.close()
        conn.close()

        # 6. Formatear los resultados en una lista simple de nombres
        # amenities_tuples es una lista de tuplas, ej:
        # La convertimos a una lista de strings, ej:
        results = [item for item in amenities_tuples]

        # 7. Devolver la lista como una respuesta JSON
        return jsonify(results)

    except Exception as e:
        # Si algo sale mal, devolvemos un error para poder depurarlo
        return jsonify({"error": "Ocurrió un error en el servidor", "details": str(e)}), 500

# Código para que Easypanel pueda ejecutar la aplicación (no se usa directamente)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
