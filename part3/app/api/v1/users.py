from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    
    if user_id != current_user['id']:
        return jsonify({"error": "Unauthorized"}), 403

    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if key in ['email', 'password', 'id', 'created_at', 'updated_at']:
            continue
        setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
