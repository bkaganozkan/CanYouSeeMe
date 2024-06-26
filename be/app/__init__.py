from flask import Flask
from flask_cors import CORS  
from flask_sqlalchemy import SQLAlchemy
from app.routes import register_routes
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    register_routes(app)


    return app

def init_app(app):
    with app.app_context():
        print("Creating all tables...")  # Debug statement to verify table creation
        db.create_all()  # This will create tables only if they don't exist
        print("Tables created.")  # Debug statement to confirm tables are created
