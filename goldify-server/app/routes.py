from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User

def setup_routes(app):
    @app.route('/')
    def home():
        return jsonify(message="Backend is running")
    
    @app.route('/me', methods=['GET'])
    @jwt_required()
    def me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return jsonify(id=user.id, username=user.username)
