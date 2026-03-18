from flask import Flask, request, jsonify
from datetime import datetime
from functools import wraps

app = Flask(__name__)

citas = []
contador = 1

USUARIO = "root"
PASSWORD = "1234"


# -----------------------------
# AUTENTICACIÓN
# -----------------------------
def verificar_auth(auth):
    return auth and auth.username == USUARIO and auth.password == PASSWORD


def requiere_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not verificar_auth(auth):
            return jsonify({"mensaje": "Acceso no autorizado"}), 401
        return f(*args, **kwargs)
    return decorated


# -----------------------------
# CREAR CITA
# -----------------------------
@app.route('/citas', methods=['POST'])
def crear_cita():
    global contador

    data = request.get_json()

    nombre = data.get("nombre")
    fecha = data.get("fecha")
    motivo = data.get("motivo")

    if not nombre or len(nombre) < 5:
        return jsonify({"error": "El nombre debe tener minimo 5 caracteres"}), 400

    if not motivo or len(motivo) > 100:
        return jsonify({"error": "El motivo no debe exceder 100 caracteres"}), 400

    try:
        fecha_cita = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Formato de fecha incorrecto (YYYY-MM-DD)"}), 400

    if fecha_cita < datetime.now().date():
        return jsonify({"error": "La fecha no puede ser menor a la fecha actual"}), 400

    citas_mismo_dia = [
        c for c in citas if c["nombre"] == nombre and c["fecha"] == fecha
    ]

    if len(citas_mismo_dia) >= 3:
        return jsonify({"error": "No se permiten mas de 3 citas el mismo dia para el mismo paciente"}), 400

    cita = {
        "id": contador,
        "nombre": nombre,
        "fecha": fecha,
        "motivo": motivo,
        "confirmado": False
    }

    citas.append(cita)
    contador += 1

    return jsonify({
        "mensaje": "Cita creada correctamente",
        "cita": cita
    }), 201


# -----------------------------
# LISTAR CITAS (PROTEGIDO)
# -----------------------------
@app.route('/citas', methods=['GET'])
@requiere_auth
def listar_citas():
    return jsonify(citas)


# -----------------------------
# CONFIRMAR CITA
# -----------------------------
@app.route('/citas/<int:id>/confirmar', methods=['PUT'])
def confirmar_cita(id):
    for cita in citas:
        if cita["id"] == id:
            cita["confirmado"] = True
            return jsonify({
                "mensaje": "Cita confirmada",
                "cita": cita
            })

    return jsonify({"error": "Cita no encontrada"}), 404


# -----------------------------
# ELIMINAR CITA (PROTEGIDO)
# -----------------------------
@app.route('/citas/<int:id>', methods=['DELETE'])
@requiere_auth
def eliminar_cita(id):
    global citas

    for cita in citas:
        if cita["id"] == id:
            citas.remove(cita)
            return jsonify({"mensaje": "Cita eliminada"})

    return jsonify({"error": "Cita no encontrada"}), 404


# -----------------------------
# EJECUTAR SERVIDOR
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)