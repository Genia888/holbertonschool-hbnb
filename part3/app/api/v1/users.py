from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import dalton as facade

api = Namespace('users', description='Users operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name':  fields.String(required=True, description='Last name'),
    'email':      fields.String(required=True, description='Email'),
    'password':   fields.String(required=True, description='Password')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        from flask import request
        data = request.get_json()
        for f in ('first_name','last_name','email','password'):
            if not data.get(f):
                return {'error': f'Missing {f}'}, 400
        if len(data['password']) < 6:
            return {'error': 'Password too short'}, 400
        user = facade.create_user(data)
        return {'message': 'User created', 'id': user.id}, 201

@api.route('/login/')
class LoginResource(Resource):
    def post(self):
        from flask import request
        data = request.get_json()
        user = facade.authenticate_user(data.get('email'), data.get('password'))
        if not user:
            return {'message': 'Invalid credentials'}, 401
        token = create_access_token(identity=user.id, additional_claims={'is_admin': False})
        return {'access_token': token}, 200

@api.route('/protected/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello user {current_user}, you are authorized'}, 200

@api.route('/login/')
class LoginResource(Resource):
    def post(self):
        from flask import request
        data = request.get_json()
        user = facade.authenticate_user(data.get('email'), data.get('password'))
        if not user:
            return {"message": "Invalid credentials"}, 401
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200

@api.route('/protected/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": "You are logged in and authorized"}, 200
