# =====================================================================
# API DE DETALLES DE PROPIEDADES - Versión 2.0
# Devuelve las características principales Y la lista de comodidades
# de un apartamento específico.
# =====================================================================

import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify

# --- PASO 1: CONFIGURACIÓN ---
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        cursor_factory=psycopg2.extras.DictCursor # Importante para obtener resultados como diccionarios
    )
    return conn

# --- PASO 2: LA HABILIDAD MEJORADA DE LA API ---

@app.route('/properties/<int:property_id>/details', methods=)
def get_property_details(property_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # --- Consulta 1: Obtener las características de la tabla 'properties' ---
        cur.execute("SELECT * FROM properties WHERE id = %s;", (property_id,))
        property_data = cur.fetchone()

        if not property_data:
            cur.close()
            conn.close()
            return jsonify({"error": "Propiedad no encontrada"}), 404

        # --- Consulta 2: Obtener las comodidades de la propiedad ---
        cur.execute("""
            SELECT a.name
            FROM amenities a
            JOIN property_amenities pa ON a.id = pa.amenity_id
            WHERE pa.property_id = %s;
        """, (property_id,))
        
        amenities_tuples = cur.fetchall()
        
        # Convertir la lista de tuplas de comodidades a una lista simple de strings
        amenities_list = [item['name'] for item in amenities_tuples]

        # --- Paso 3: Combinar toda la información ---
        # Convertimos los datos de la propiedad a un diccionario estándar
        details = dict(property_data)
        # Añadimos la lista de comodidades al diccionario
        details['amenities'] = amenities_list

        cur.close()
        conn.close()

        # Devolvemos el objeto JSON completo
        return jsonify(details)

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
