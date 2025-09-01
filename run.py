# =====================================================================
# API DE DETALLES DE PROPIEDADES - Versión 3.0 (Final)
# Devuelve una respuesta limpia, traducida y formateada para el usuario.
# =====================================================================

import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify

# --- PASO 1: CONFIGURACIÓN (Sin cambios) ---
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        cursor_factory=psycopg2.extras.DictCursor
    )
    return conn

# --- PASO 2: LA HABILIDAD REFINADA DE LA API ---

@app.route('/properties/<int:property_id>/details', methods=['GET'])
def get_property_details(property_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # --- Consulta 1: Obtener todos los datos de la propiedad (sin cambios) ---
        cur.execute("SELECT * FROM properties WHERE id = %s;", (property_id,))
        property_data_raw = cur.fetchone()

        if not property_data_raw:
            cur.close()
            conn.close()
            return jsonify({"error": "Propiedad no encontrada"}), 404

        # --- Consulta 2: Obtener las comodidades (sin cambios) ---
        cur.execute("""
            SELECT a.name
            FROM amenities a
            JOIN property_amenities pa ON a.id = pa.amenity_id
            WHERE pa.property_id = %s;
        """, (property_id,))
        
        amenities_tuples = cur.fetchall()
        amenities_list = [item['name'] for item in amenities_tuples]

        cur.close()
        conn.close()

        # --- PASO 3: LA MAGIA - CONSTRUIR LA RESPUESTA LIMPIA Y TRADUCIDA ---
        # Creamos un diccionario vacío que será nuestra respuesta final.
        detalles_limpios = {}

        # Llenamos el diccionario solo con los campos que queremos y con claves en español.
        detalles_limpios['nombre'] = property_data_raw['name']
        detalles_limpios['descripcion'] = property_data_raw['description']
        detalles_limpios['direccion'] = property_data_raw['address']
        detalles_limpios['barrio'] = property_data_raw['neighborhood']
        detalles_limpios['nombre_edificio'] = property_data_raw['building_name']
        detalles_limpios['piso'] = property_data_raw['floor_level']
        detalles_limpios['tipo_propiedad'] = property_data_raw['property_type']
        detalles_limpios['numero_habitaciones'] = property_data_raw['num_bedrooms']
        detalles_limpios['numero_banos'] = property_data_raw['num_bathrooms']
        detalles_limpios['maximo_huespedes'] = property_data_raw['max_guests']
        
        # Lógica para el balcón: solo lo mencionamos si tiene.
        if property_data_raw['has_balcony']:
            detalles_limpios['balcon'] = f"Sí, tiene {property_data_raw['num_balconies']} balcón(es)."
        
        # Finalmente, añadimos la lista de comodidades que ya teníamos.
        detalles_limpios['comodidades'] = amenities_list

        # NOTA: Campos como 'id', 'is_active', 'latitude', 'longitude' nunca se añaden
        # al diccionario 'detalles_limpios', por lo que no se expondrán al exterior.

        # Devolvemos el objeto JSON limpio y traducido
        return jsonify(detalles_limpios)

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
