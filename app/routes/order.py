from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal

from app.extensions import db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User

order_bp = Blueprint("orders", __name__, url_prefix="/orders")

@order_bp.route("", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json() or {}

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or not quantity:
        return jsonify({"error": "product_id and quantity are required"}), 400

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "quantity must be a positive integer"}), 400

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "user not found"}), 404

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    if product.stock < quantity:
        return jsonify({"error": "insufficient product stock"}), 400

    total_price = product.price * Decimal(quantity)

    product.stock -= quantity

    order = Order(
        user_id=user.id,
        product_id=product.id,
        quantity=quantity,
        total_price=total_price
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "order_id": order.id,
        "user_id": user.id,
        "product_id": product.id,
        "quantity": order.quantity,
        "total_price": str(order.total_price),
        "status": order.status,
    }), 201

@order_bp.route("", methods=["GET"])
@jwt_required()
def list_orders():
    user_id = int(get_jwt_identity())

    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": o.id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": str(o.total_price),
            "status": o.status,
            "created_at": o.created_at.isoformat()
        }
        for o in orders
    ])