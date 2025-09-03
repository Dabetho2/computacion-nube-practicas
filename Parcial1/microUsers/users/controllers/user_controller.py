from flask import Blueprint, request, jsonify, session
from db.db import db
from users.models.user_model import Users  # <- tu modelo (plural)

user_controller = Blueprint("user_controller", __name__)

# --------------------------------------------------------------------
# Listar usuarios
# --------------------------------------------------------------------
@user_controller.route("/api/users", methods=["GET"])
def get_users():
    users = Users.query.all()
    result = [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "username": u.username
    } for u in users]
    return jsonify(result), 200


# --------------------------------------------------------------------
# Obtener usuario por id
# --------------------------------------------------------------------
@user_controller.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    u = Users.query.get_or_404(user_id)
    return jsonify({
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "username": u.username
    }), 200


# --------------------------------------------------------------------
# Crear usuario
# --------------------------------------------------------------------
@user_controller.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    for k in ("name", "email", "username", "password"):
        if k not in data:
            return jsonify({"message": f"'{k}' requerido"}), 400
    nu = Users(
        name=data["name"],
        email=data["email"],
        username=data["username"],
        password=data["password"]   # simple (sin hash) como venías usando
    )
    db.session.add(nu)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# --------------------------------------------------------------------
# Actualizar usuario
# --------------------------------------------------------------------
@user_controller.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    u = Users.query.get_or_404(user_id)
    data = request.get_json() or {}
    if "name" in data:     u.name = data["name"]
    if "email" in data:    u.email = data["email"]
    if "username" in data: u.username = data["username"]
    if "password" in data: u.password = data["password"]
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


# --------------------------------------------------------------------
# Borrar usuario
# --------------------------------------------------------------------
@user_controller.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    u = Users.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# --------------------------------------------------------------------
# Login sencillo (sin hash, devuelve 401 en fallo, no 500)
# --------------------------------------------------------------------
@user_controller.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = Users.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Guarda en sesión (opcional pero útil)
    session['user_id'] = user.id
    session['username'] = user.username
    session['email'] = user.email

    # Devuelve datos para que el frontend los guarde
    return jsonify({
        'message': 'Login successful',
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200
