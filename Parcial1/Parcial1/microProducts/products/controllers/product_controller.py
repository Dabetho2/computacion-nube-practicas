from flask import Blueprint, request, jsonify
from db.db import db
from products.models.product_model import Products

product_controller = Blueprint("product_controller", __name__)

def to_dict(p: Products):
    return {"id": p.id, "name": p.name, "price": p.price, "quantity": p.quantity}

@product_controller.get("/api/products")
def list_products():
    return jsonify([to_dict(p) for p in Products.query.all()])

@product_controller.get("/api/products/<int:pid>")
def get_product(pid):
    p = Products.query.get_or_404(pid)
    return jsonify(to_dict(p))

@product_controller.post("/api/products")
def create_product():
    data = request.get_json() or {}
    for k in ("name", "price", "quantity"):
        if k not in data:
            return jsonify({"message": f"'{k}' requerido"}), 400
    p = Products(name=data["name"], price=data["price"], quantity=data["quantity"])
    db.session.add(p); db.session.commit()
    return jsonify({"message": "created", "id": p.id}), 201

@product_controller.put("/api/products/<int:pid>")
def update_product(pid):
    p = Products.query.get_or_404(pid)
    data = request.get_json() or {}
    for k in ("name", "price", "quantity"):
        if k not in data:
            return jsonify({"message": f"'{k}' requerido"}), 400
    p.name = data["name"]; p.price = data["price"]; p.quantity = data["quantity"]
    db.session.commit()
    return jsonify({"message": "updated"})

@product_controller.delete("/api/products/<int:pid>")
def delete_product(pid):
    p = Products.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    return jsonify({"message": "deleted"})

# usado por órdenes: delta negativo descuenta
@product_controller.post("/api/products/<int:pid>/adjust")
def adjust_stock(pid):
    p = Products.query.get_or_404(pid)
    delta = int((request.get_json() or {}).get("delta", 0))
    if p.quantity + delta < 0:
        return jsonify({"error": "stock_insufficient", "available": p.quantity}), 409
    p.quantity += delta
    db.session.commit()
    return jsonify({"message": "ok", "quantity": p.quantity})
