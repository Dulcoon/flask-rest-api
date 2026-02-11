from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "email": user.email
    })
