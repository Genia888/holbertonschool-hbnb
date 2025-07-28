from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place_reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                }
                for review in place_reviews
            ], 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input or unauthorized')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self, place_id):
        """Add a review to a specific place"""
        review_data = api.payload
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not review_data.get('text') or not review_data.get('rating'):
            return {'message': 'Missing required fields'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner == user_id:
            return {'error': 'You cannot review your own place'}, 400

        existing_reviews = facade.get_reviews_by_place(place_id)
        if not is_admin and any(r.user_id == user_id for r in existing_reviews):
            return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(
                review_data,
                user_id,
                review_data['rating'],
                place_id
            )
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400