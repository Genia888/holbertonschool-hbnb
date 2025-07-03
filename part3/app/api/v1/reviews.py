from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.review import Review
from models.place import Place

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('', methods=['POST'])
@jwt_required()
def create_review():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data or 'place_id' not in data or 'text' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    place = storage.get(Place, data['place_id'])
    if not place:
        return jsonify({"error": "Place not found"}), 404

    # íº« Interdit de reviewer son propre lieu
    if place.owner_id == current_user['id']:
        return jsonify({"error": "Cannot review your own place"}), 403

    # íº« Interdit de reviewer deux fois le mÃªme lieu
    existing_reviews = storage.all(Review)
    for review in existing_reviews.values():
        if review.place_id == data['place_id'] and review.user_id == current_user['id']:
            return jsonify({"error": "You have already reviewed this place"}), 403

    new_review = Review(**data)
    new_review.user_id = current_user['id']
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user = get_jwt_identity()
    review = storage.get(Review, review_id)

    if not review:
        return jsonify({"error": "Review not found"}), 404

    if review.user_id != current_user['id']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
