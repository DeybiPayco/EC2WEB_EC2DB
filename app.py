from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# ========== CONFIG MYSQL DESDE ENV ===========
app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT", 3306))
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# ====================================
# 🏠 Ruta principal (formulario)
# ====================================
@app.route('/')
def contacto():
    return render_template('contacto.html')


# ====================================
# 📄 Ruta lista
# ====================================
@app.route('/lista')
def lista():
    return render_template('lista.html')


# ====================================
# 📌 API: Guardar contacto
# ====================================
@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.get_json()

    nombre = data.get("nombre", "").strip()
    correo = data.get("correo", "").strip()
    telefono = data.get("telefono", "").strip()

    # --------------------------
    # Validación backend
    # --------------------------
    if len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener mínimo 3 caracteres."}), 400

    if "@" not in correo:
        return jsonify({"error": "Correo inválido."}), 400

    if telefono and not telefono.isdigit():
        return jsonify({"error": "El teléfono debe contener solo números."}), 400

    try:
        cur = mysql.connection.cursor()

        # Intentar insertar
        cur.execute("""
            INSERT INTO contactos (nombre, correoElectronico, telefono)
            VALUES (%s, %s, %s)
        """, (nombre, correo, telefono))

        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Contacto guardado correctamente."}), 200

    except MySQLdb.IntegrityError as err:
        # Error por correo duplicado
        if "Duplicate entry" in str(err):
            return jsonify({"error": "El correo ya está registrado."}), 409

        return jsonify({"error": "Error de integridad en la BD."}), 500

    except Exception as e:
        print("ERROR MYSQL:", e)
        return jsonify({"error": "Error al guardar en la base de datos."}), 500


# ====================================
# 📌 API: Obtener contactos
# ====================================
@app.route('/api/contactos', methods=['GET'])
def obtener_contactos():
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT id, nombre, correoElectronico, telefono, fechaRegistro
            FROM contactos
            ORDER BY id DESC
        """)

        datos = cur.fetchall()
        cur.close()

        return jsonify(datos), 200

    except Exception as e:
        print("ERROR MYSQL:", e)
        return jsonify({"error": "Error al obtener contactos."}), 500


# ====================================
# 🚀 Ejecutar servidor
# ====================================
if __name__ == '__main__':
    app.run(debug=True)
