from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from decimal import Decimal, InvalidOperation

from app.extensions import db
from app.models.product import Product

product_bp = Blueprint("products", __name__, url_prefix="/products")

@product_bp.route("", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json() or {}

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:
        return jsonify({"error": "name, price, and stock are required"}), 400

    try:
        price = Decimal(price)
        if price < 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return jsonify({"error": "price must be a valid decimal string"}), 400

    if not isinstance(stock, int) or stock < 0:
        return jsonify({"error": "stock must be a non-negative integer"}), 400

    product = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock
    }), 201


@product_bp.route("", methods=["GET"])
def list_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "stock": p.stock
        }
        for p in products
    ]), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock
    }), 200


@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    data = request.get_json() or {}

    if "name" in data:
        product.name = data["name"]

    if "price" in data:
        try:
            product.price = Decimal(data["price"])
            if product.price < 0:
                raise InvalidOperation
        except (InvalidOperation, TypeError):
            return jsonify({"error": "price must be a valid decimal string"}), 400

    if "stock" in data:
        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return jsonify({"error": "stock must be a non-negative integer"}), 400
        product.stock = data["stock"]

    db.session.commit()

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock
    }), 200

@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "product deleted"}), 200
