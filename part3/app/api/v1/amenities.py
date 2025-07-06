from flask_restx import Namespace, Resource

ns = Namespace('amenities', description='Amenities operations')

@ns.route('/ping')
class Ping(Resource):
    def get(self):
        return {'message': 'pong'}
