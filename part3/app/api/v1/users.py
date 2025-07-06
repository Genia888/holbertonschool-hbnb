from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

ns = Namespace("users", description="User operations")

user_model = ns.model("User", {
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String(readOnly=True),
    "password": fields.String(readOnly=True),
})

USERS = {
    "fake-user-id": {
        "email": "admin@hbnb.com",
        "first_name": "Admin",
        "last_name": "User",
        "password": "admin"
    }
}

@ns.route("/me")
class UserMe(Resource):
    @ns.doc(security='apikey')
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return USERS.get(identity), 200

    @ns.doc(security='apikey')
    @jwt_required()
    @ns.expect(user_model)
    def put(self):
        identity = get_jwt_identity()
        user = USERS.get(identity)
        if not user:
            return {"error": "User not found"}, 404
        data = ns.payload
        # Interdit la modif email & password
        data.pop("email", None)
        data.pop("password", None)
        user.update(data)
        return {"message": "User updated", "user": user}, 200
