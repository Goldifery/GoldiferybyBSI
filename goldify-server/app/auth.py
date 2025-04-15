from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .models import User
from . import db
from app.utils.response import success_response, error_response
from app.utils.validators import is_valid_email, is_strong_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not name or not email or not phone or not password:
        return error_response("Name, email, phone, and password are required", 400)

    if not is_valid_email(email):
        return error_response("Invalid email format", 400)

    if not is_strong_password(password):
        return error_response(
            "Password must be at least 8 characters long, contain uppercase, lowercase, number, and symbol.",
            400
        )

    if User.query.filter_by(email=email).first():
        return error_response("Email already registered", 409)

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, phone=phone, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return success_response("User created", {
        "name": new_user.name,
        "email": new_user.email,
        "phone": new_user.phone
    }, 201)



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Email and password are required", 400)

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return success_response("Login successful", {
            "access_token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone
            }
        })

    return error_response("Invalid credentials", 401)

