from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import request

api = Namespace('admin', description='Admin operations')

user_model = api.model(
    'User', {
        'first_name': fields.String(
            required=True, description='First name of the user'),
        'last_name': fields.String(
            required=True, description='Last name of the user'),
        'password': fields.String(
            required=True, description='User\'s password'),
        'email': fields.String(
            required=True, description='Email of the user'),
        'is_admin': fields.Boolean(
            required=True, description='Admin flag')
    }
)

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    @jwt_required()
    def post(self):
        user_data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    @jwt_required()
    def put(self, user_id):
        user_data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'id': updated_user.id,
                'message': 'User successfully updated',
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except TypeError as e:
            return {'error': str(e)}, 400


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        amenity_data = api.payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            existing_amenity = facade.get_amenity_by_name(
                amenity_data['name'])
            if existing_amenity:
                return {'error': 'Amenity already registered'}, 400
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'message': 'Amenity successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    @jwt_required()
    def put(self, amenity_id):
        amenity_data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'message': 'Amenity successfully updated'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400