from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')
api = Namespace('admin', description='Admin operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        # Step 1: Retrieve the user by email
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.check_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Step 2: Create JWT token
        access_token = create_access_token(
            identity=str(user.id),  # identity must be a string
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200


# Example protected endpoint to verify JWT
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Token is valid')
    def get(self):
        """Example of a protected endpoint"""
        user_id = get_jwt_identity()  # identity is now a string
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        return {
            'message': f"Hello, user {user_id} (Admin: {is_admin})"
        }, 200
    
@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            #Chek if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != user_id:
                return {'error': 'Email is already in use'}, 400

        #Logic of updating user
        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found or update failed'}, 404

        return {
            'message': 'User updated successfully',
            'user': updated_user.to_dict()
        }, 200