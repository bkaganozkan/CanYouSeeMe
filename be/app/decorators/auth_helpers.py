from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request,decode_token, get_jwt, get_jwt_identity


def is_token_revoked(jwt_header, jwt_payload):
    from app.models import TokenBlocklist
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None


def role_required(*required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                user_role = current_user.get('role')
                if not current_user or not user_role:
                    return jsonify({'message': 'Unauthorized: User identity or role not found'}), 401

                if user_role not in required_roles:
                    return jsonify({'message': 'Unauthorized: Insufficient role'}), 403
            except Exception as e:
                return jsonify({'message': 'Unauthorized', 'error': str(e)}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            decode_token(token)
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 403
        return f(*args, **kwargs)
    return decorated_function