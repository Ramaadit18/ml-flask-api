import os
import jwt
from functools import wraps
from flask import request, jsonify, g
from dotenv import load_dotenv

load_dotenv()

# Secret key for JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("Secret Key environment variable not set")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        try:
            # Verify and decode the token
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = data.get('id')
            if not user_id:
                return jsonify({'message': 'Token does not contain user ID!'}), 401
            g.user_id = user_id  # Set the user_id in Flask's g object
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated
