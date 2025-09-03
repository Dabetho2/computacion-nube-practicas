from flask import Blueprint, request, jsonify, current_app, session
from decimal import Decimal
import requests

from db.db import db
from orders.models.order_model import Order

order_controller = Blueprint("order_controller", __name__)

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def _products_base():
    return current_app.config.get("PRODUCTS_BASE", "http://127.0.0.1:5003")

def _get_user_from_payload_or_session(data):
    user = data.get("user") or {}
    name = data.get("userName") or user.get("name") or session.get("username")
    email = data.get("userEmail") or user.get("email") or session.get("email")
    return name, email

# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------
@order_controller.route("/api/orders", methods=["GET"])
def get_all_orders():
    items = Order.query.order_by(Order.id.desc()).all()
    return jsonify([o.to_dict() for o in items])

@order_controller.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    o = Order.query.get_or_404(order_id)
    return jsonify(o.to_dict())

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json(silent=True) or {}

    # 1) usuario desde el body (formatos tolerantes)
    u = data.get('user') or {}
    user_name  = u.get('name') or u.get('username') or data.get('userName')
    user_email = u.get('email') or data.get('userEmail')

    # 2) override opcional por headers (por si el body no llegó)
    user_name  = request.headers.get('X-User-Name', user_name)
    user_email = request.headers.get('X-User-Email', user_email)

    if not user_name or not user_email:
        return jsonify({
            'message': 'Información de usuario inválida',
            'debug': {'body_user': u, 'top': {'userName': data.get('userName'),
                                              'userEmail': data.get('userEmail')}}
        }), 400

    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400
    # Productos
    products = data.get("products")
    if not products or not isinstance(products, list):
        return jsonify({"message": "Falta o es inválida la información de los productos"}), 400

    # Validación y cálculo del total
    base = _products_base()
    total = Decimal("0")
    items = []

    for item in products:
        try:
            pid = int(item.get("id"))
            qty = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            return jsonify({"message": "Producto/quantidad inválidos"}), 400

        if qty <= 0:
            continue

        # Traer producto
        try:
            r = requests.get(f"{base}/api/products/{pid}", timeout=5)
        except requests.RequestException:
            return jsonify({"message": "Productos no disponible"}), 503

        if r.status_code != 200:
            return jsonify({"message": "Productos no disponible"}), 503

        p = r.json()
        if p.get("quantity", 0) < qty:
            return jsonify(
                {"message": f"Sin stock para {p.get('name')}", "available": p.get("quantity", 0)}
            ), 409

        price = Decimal(str(p.get("price", 0)))
        total += price * qty
        items.append((pid, qty))

    if not items:
        return jsonify({"message": "No se enviaron cantidades válidas"}), 400

    # Descontar inventario
    adjusted = []
    for pid, qty in items:
        try:
            a = requests.post(f"{base}/api/products/{pid}/adjust",
                              json={"delta": -qty}, timeout=5)
        except requests.RequestException:
            a = None

        if not a or a.status_code != 200:
            # *Opcional*: rollback de ajustes previos
            for pprev, qprev in adjusted:
                try:
                    requests.post(f"{base}/api/products/{pprev}/adjust",
                                  json={"delta": qprev}, timeout=5)
                except requests.RequestException:
                    pass
            return jsonify({"message": "No se pudo actualizar inventario"}), 503

        adjusted.append((pid, qty))

    # Guardar orden
    o = Order(userName=user_name, userEmail=user_email, saleTotal=total)
    db.session.add(o)
    db.session.commit()

    return jsonify({"message": "Orden creada exitosamente", "order_id": o.id}), 201
