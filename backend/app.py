import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONEXIÓN A BASE DE DATOS ---
def obtener_conexion_bd():
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'), 
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'stockmaster_db')
    )
    return conn

@app.route('/')
def inicio():
    return jsonify({"mensaje": "API StockMaster (MySQL) Funcionando"})

# --- 1. LEER PRODUCTOS ---
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
        return jsonify({"error": "Error de conexión"}), 500

# --- 2. CREAR PRODUCTO ---
@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    try:
        nuevo_producto = request.get_json()
        conn = obtener_conexion_bd()
        cur = conn.cursor()
        
        sql = 'INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)'
        val = (nuevo_producto['nombre'], nuevo_producto['descripcion'], nuevo_producto['precio'], nuevo_producto['stock'])
        
        cur.execute(sql, val)
        conn.commit()
        
        nuevo_id = cur.lastrowid
        
        cur.close()
        conn.close()
        return jsonify({"id": nuevo_id, "mensaje": "Producto creado"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al guardar"}), 500

# --- 3. ACTUALIZAR PRODUCTO ---
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        datos = request.get_json()
        conn = obtener_conexion_bd()
        cur = conn.cursor()
        sql = 'UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s'
        val = (datos['nombre'], datos['descripcion'], datos['precio'], datos['stock'], id)
        
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al actualizar"}), 500

# --- 4. ELIMINAR PRODUCTO ---
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = obtener_conexion_bd()
        cur = conn.cursor()
        cur.execute('DELETE FROM productos WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Eliminado"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al eliminar"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)