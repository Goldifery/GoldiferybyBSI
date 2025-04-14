from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
import time
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .routes import setup_routes
    setup_routes(app)  

    with app.app_context():
        MAX_RETRIES = 10
        for i in range(MAX_RETRIES):
            try:
                db.create_all()
                print("✅ DB connected")
                break
            except OperationalError as e:
                print(f"⏳ DB not ready ({i+1}/{MAX_RETRIES}): {e}")
                time.sleep(3)

    return app
