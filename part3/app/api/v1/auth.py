from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services.facade import facade

auth_ns = Namespace('auth', description='Authentication operations')

# --- Authentification : login ---
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = request.json
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.check_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200


# --- Récupérer l'utilisateur connecté ---
@auth_ns.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        """Retourne les infos de l'utilisateur connecté via JWT"""
        user_id = get_jwt_identity()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200


# --- Endpoint protégé (test) ---
@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        return {'message': f"Hello, user {user_id} (Admin: {is_admin})"}, 200


# --- Admin : mise à jour d'un utilisateur ---
@auth_ns.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != user_id:
                return {'error': 'Email is already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found or update failed'}, 404

        return {'message': 'User updated successfully', 'user': updated_user.to_dict()}, 200