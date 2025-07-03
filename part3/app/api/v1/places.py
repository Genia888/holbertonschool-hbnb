from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.place import Place

places_bp = Blueprint('places', __name__, url_prefix='/places')


@places_bp.route('', methods=['POST'])
@jwt_required()
def create_place():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    data['owner_id'] = current_user['id']
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@places_bp.route('/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    current_user = get_jwt_identity()
    place = storage.get(Place, place_id)

    if not place:
        return jsonify({"error": "Place not found"}), 404

    if place.owner_id != current_user['id']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'owner_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@places_bp.route('/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    current_user = get_jwt_identity()
    place = storage.get(Place, place_id)

    if not place:
        return jsonify({"error": "Place not found"}), 404

    if place.owner_id != current_user['id']:
        return jsonify({"error": "Unauthorized"}), 403

    storage.delete(place)
    storage.save()
    return '', 204
