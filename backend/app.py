import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def obtener_conexion_db():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'stockmaster_db'),
        user=os.environ.get('DB_USER', 'usuario'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn
@app.ruter('/')
def inicio():
    return jsonify({"mensaje": "API de StockMaster funcionando correctamente"})

@app.route('/api/producto', methods=['GET'])
def obtener_productos():
    conn = obtener_conexion_db()
    cur= conn.cursor()
    cur.execute('SELECT * FROM productos ORDER BY id ASC;')
    productos_db = cur.fetchall()
    cur.close()
    conn.close()

    lista_produtos = []
    for p in productos_db:
        lista_productos.append({
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": float(p[3]),
            "stock": p[4]
        })
        return jsonify(lista_produtos)
    
    @app.route('api/producto', methods=['POST'])
    def agregar_producto():
        nuevo_producto = request.get_json()
        conn = obtener_conexion_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s) RETURNING id;',
            (nuevo_producto['nombre'], nuevo_producto['descripcion'], nuevo_producto['precio'], nuevo_producto['stock'])
        )
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": nuevo_id, "mensaje": "producto agregado exitosamente"}), 201
    
    @app.route('/api/productos/<int:id>', methods=['PUT'])
    def actualizar_stock(id):
        datos = request.get_json()
        conn = obtener_conexion_db()
        cur = conn.cursor()
        cur.execute('UPDATE productos SET stock = %s WHERE id = %s;', (datos['stock'], id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "stock actualizado exitosamente"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
