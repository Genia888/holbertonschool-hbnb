from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import PLACES

ns = Namespace("reviews", description="Operations on reviews")

review_model = ns.model("Review", {
    "id": fields.String(readOnly=True),
    "place_id": fields.String(required=True),
    "text": fields.String(required=True),
    "user_id": fields.String(readOnly=True),
})

REVIEWS = []
REVIEW_ID = 1

@ns.route("/")
class ReviewList(Resource):
    @ns.doc(security='apikey')
    @jwt_required()
    @ns.expect(review_model, validate=True)
    def post(self):
        global REVIEW_ID
        if not request.is_json:
            return {"error": "Missing JSON in request"}, 400
        data = request.get_json()
        place_id = data.get("place_id")
        text = data.get("text")
        user_id = get_jwt_identity()
        place_owner_id = None
        for p in PLACES:
            if p["id"] == place_id:
                place_owner_id = p["user_id"]
                break
        if place_owner_id is None:
            return {"error": "Place not found"}, 404
        if place_owner_id == user_id:
            return {"error": "You can't review your own place"}, 400
        for r in REVIEWS:
            if r["place_id"] == place_id and r["user_id"] == user_id:
                return {"error": "You already reviewed this place"}, 400
        review = {
            "id": str(REVIEW_ID),
            "place_id": place_id,
            "text": text,
            "user_id": user_id
        }
        REVIEW_ID += 1
        REVIEWS.append(review)
        return {"message": "Review created", "review": review}, 201

    @ns.doc(security='apikey')
    @jwt_required()
    def get(self):
        return REVIEWS, 200

@ns.route("/<string:review_id>")
class ReviewItem(Resource):
    @ns.doc(security='apikey')
    @jwt_required()
    def put(self, review_id):
        if not request.is_json:
            return {"error": "Missing JSON in request"}, 400
        data = request.get_json()
        for rev in REVIEWS:
            if rev["id"] == review_id and rev["user_id"] == get_jwt_identity():
                rev["text"] = data.get("text", rev["text"])
                return {"message": "Review updated", "review": rev}, 200
        return {"message": "Review not found or forbidden"}, 404

    @ns.doc(security='apikey')
    @jwt_required()
    def delete(self, review_id):
        for rev in REVIEWS:
            if rev["id"] == review_id and rev["user_id"] == get_jwt_identity():
                REVIEWS.remove(rev)
                return {"message": "Review deleted"}, 200
        return {"message": "Review not found or forbidden"}, 404
