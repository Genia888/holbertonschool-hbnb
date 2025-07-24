from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def post(self):
        """Register a new amenity (Admins only)"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admins only'}, 403
        
        data = api.payload
        if not data.get("name"):
            return {'message': 'Name is required'}, 400
        try:
            new_amenity = facade.create_amenity(data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities (public)"""
        try:
            amenities = facade.get_all_amenities()
            return [a.to_dict() for a in amenities], 200
        except Exception as e:
            return {'message': str(e)}, 500

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (public)"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {'message': 'Amenity not found'}, 404

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (Admins only)"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admins only'}, 403

        data = api.payload
        try:
            updated = facade.update_amenity(amenity_id, data)
            if updated:
                return updated.to_dict(), 200
            return {'message': 'Amenity not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 400
        
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Admin only: Create a new amenity"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        name = data.get('name')

        if not name:
            return {'error': 'Amenity name is required'}, 400

        try:
            new_amenity = facade.create_amenity(data)
            if not new_amenity:
                return {'error': 'Amenity creation failed'}, 500

            return {
                'message': 'Amenity created successfully',
                'amenity': {
                    'id': new_amenity.id,
                    'name': new_amenity.name
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400
        
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Admin only: Modify an existing amenity"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        name = data.get('name')

        if not name:
            return {'error': 'Amenity name is required'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if not updated_amenity:
                return {'error': 'Amenity not found or update failed'}, 404

            return {
                'message': 'Amenity updated successfully',
                'amenity': {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400
