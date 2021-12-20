"""
API for handling authentication.
"""
import json

from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager

from server.database import interface

auth_api = Blueprint('auth_api', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Returns True if token is revoked.
    """
    jti = jwt_payload['jti']
    return interface.is_revoked(jti)


@auth_api.route('/login', methods=['POST'])
def login():
    """
    Logs in a user.
    """
    data = json.loads(request.data)

    user_email = data['email']
    password = data['password']

    user = interface.get_user_by_email(user_email)

    # If user exists and correct password
    if user and bcrypt.check_password_hash(user.pw_hash, password):
        token = create_access_token(identity=user.id)
        return {'token': token}, 200

    return {'msg': 'Wrong email or password'}, 401


@auth_api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logs out the user.
    """
    jti = get_jwt()['jti']
    interface.revoke_token(jti)

    return {'msg': 'Access token revoked'}, 200


@auth_api.route('/check', methods=['POST'])
@jwt_required()
def check():
    """
    Checks if the user is authenticated.
    """
    return {'msg': 'Access'}, 200
