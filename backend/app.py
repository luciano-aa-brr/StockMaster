import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def obtener_conexion_bd():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'stockmaster_db'),
        user=os.environ.get('DB_USER', 'usuario'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn


@app.route('/')
def inicio():
    return jsonify({"mensaje": "API de StockMaster funcionando correctamente"})


@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        conn = obtener_conexion_bd()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos ORDER BY id ASC;')
        productos_bd = cur.fetchall()
        cur.close()
        conn.close()
        
        lista_productos = []
        for p in productos_bd:
            lista_productos.append({
                "id": p[0],
                "nombre": p[1],
                "descripcion": p[2],
                "precio": float(p[3]),
                "stock": p[4]
            })
        return jsonify(lista_productos)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al conectar con la base de datos"}), 500


@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    try:
        nuevo_producto = request.get_json()
        conn = obtener_conexion_bd()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s) RETURNING id;',
            (nuevo_producto['nombre'], nuevo_producto['descripcion'], nuevo_producto['precio'], nuevo_producto['stock'])
        )
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": nuevo_id, "mensaje": "Producto creado exitosamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al guardar el producto"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)