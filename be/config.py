import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///drone_database.db'  # SQLite database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True,  
        'connect_args': {'timeout': 30}
    }
    SQLALCHEMY_BINDS = {'drones_db': 'sqlite:///drone_database.db'}
    FLASK_ENV = 'development'
    JWT_SECRET_KEY = 'top_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) 
    SERVER_URL="http://localhost:5000"
