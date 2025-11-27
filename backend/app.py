import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
# Importamos las herramientas de seguridad
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Configuración de JWT (Tokens)
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', 'clave-segura-por-defecto')
jwt = JWTManager(app)

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
    return jsonify({"mensaje": "API StockMaster Segura Funcionando"})

# ==========================================
#  AUTENTICACIÓN (LOGIN Y REGISTRO)
# ==========================================

# 1. REGISTRO DE USUARIO
@app.route('/api/register', methods=['POST'])
def registrar_usuario():
    try:
        datos = request.get_json()
        email = datos.get('email')
        password = datos.get('password')
        nombre = datos.get('nombre')
        nombre_negocio = datos.get('nombre_negocio')

        if not email or not password or not nombre_negocio:
            return jsonify({"error": "Faltan datos (email, pass, nombre o negocio)"}), 400

        password_encriptada = generate_password_hash(password)

        conn = obtener_conexion_bd()
        cur = conn.cursor()
        
        # Guardamos el nombre_negocio en la BD
        sql = 'INSERT INTO usuarios (nombre, email, password_hash, nombre_negocio) VALUES (%s, %s, %s, %s)'
        cur.execute(sql, (nombre, email, password_encriptada, nombre_negocio))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return jsonify({"error": "El correo ya está registrado"}), 409
        print(err)
        return jsonify({"error": "Error al registrar"}), 500

# 2. INICIAR SESIÓN (LOGIN)
@app.route('/api/login', methods=['POST'])
def login():
    try:
        datos = request.get_json()
        email = datos.get('email')
        password = datos.get('password')

        conn = obtener_conexion_bd()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['password_hash'], password):
            access_token = create_access_token(identity=usuario['id'])
            return jsonify({
                "mensaje": "Login exitoso",
                "token": access_token,
                "usuario": usuario['nombre'],
                # Enviamos también el nombre del negocio al frontend
                "negocio": usuario['nombre_negocio']
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(e)
        return jsonify({"error": "Error en el servidor"}), 500


# ==========================================
#  RUTAS DE PRODUCTOS (CRUD)
# ==========================================

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    # Aquí en el futuro agregaremos @jwt_required() para proteger la ruta
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