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

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        user_id = get_jwt_identity()
        place_id = review_data['place_id']
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not review_data.get('text') or not review_data.get('rating') or not review_data.get('place_id'):
            return {'message': 'Missing required fields'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Prevent reviewing own place (unless admin)
        if not is_admin and place.owner == user_id:
            return {'error': 'You cannot review your own place'}, 400

        # Prevent multiple reviews (unless admin)
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

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review_data = api.payload

        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            if review.user_id != user_id and not is_admin:
                return {'error': 'Unauthorized action'}, 403

            if 'user_id' in review_data or 'place_id' in review_data:
                return {'error': 'You cannot modify user_id or place_id'}, 400
            
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            if review.user_id != user_id and not is_admin:
                return {'error': 'Unauthorized action'}, 403
            
            result = facade.delete_review(review_id)
            return result, 200
        except ValueError as e:
            return {'error': str(e)}, 404

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