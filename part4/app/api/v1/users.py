from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services.facade import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password (hashed before saving)'),
    'is_admin': fields.Boolean(required=False, description='Is the user an admin', default=False)
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data.get("email") or "@" not in user_data["email"]:
            return {"error": "Invalid email"}, 400

        if not user_data.get("first_name") or not user_data.get("last_name"):
            return {"error": "Missing first name or last name"}, 400

        if not user_data.get("password") or len(user_data["password"]) < 6:
            return {"error": "Password must be at least 6 characters"}, 400

        # Check for existing email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid update request')
    @jwt_required()
    def put(self, user_id):
        """Update user profile (excluding email and password)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload

        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password.'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):
        """Admin only: Create a new user"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Chek email
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'message': 'User created successfully',
                'user': {
                    'id': new_user.id,
                    'email': new_user.email,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'is_admin': new_user.is_admin
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Admin only: Modify any user's information (including email & password)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Chek email
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found or update failed'}, 404

            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'email': updated_user.email,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'is_admin': updated_user.is_admin
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400
