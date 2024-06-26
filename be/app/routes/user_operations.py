from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.models import User, TokenBlocklist
from flask_bcrypt import Bcrypt, check_password_hash

bp = Blueprint("user_operations", __name__, url_prefix="/api")

bcrypt = Bcrypt()

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        role = data.get("role", "user")
        new_user = User(username=data["username"], password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Register Error", "error": str(e)}), 400
    return jsonify({"message": "User created successfully"}), 201

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        return jsonify({"message": "Login Error", "error": str(e)})
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify(access_token=access_token, user_role=user.role ), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Logout Error", "error": str(e)}), 400
    return jsonify(msg="Successfully logged out"), 200


