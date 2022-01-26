"""
API for handling users.
"""
import json

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.database import interface
from server.routes.auth import bcrypt

user_api = Blueprint('user_api', __name__)


@user_api.route('/create', methods=['POST'])
def create():
    """
    Creates a new user.
    """
    data = json.loads(request.data)

    user_name = data['user_name']
    email = data['email']
    password = data['password']

    if interface.get_user_by_email(email):
        return {'msg': "Email already in use"}, 409

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    interface.create_user(user_name, email, password_hash)

    return '', 200


@user_api.route('/search', methods=['POST'])
@jwt_required()
def search():
    """
    Searches for users with their name. Excludes the logged in user.
    """
    data = json.loads(request.data)

    search_term = data['search_term']
    this_user = interface.get_user_by_id(get_jwt_identity())

    users = interface.search_users(search_term)

    result = [user.get_public_data() for user in users if not user.id == this_user.id]

    return {"result": result}, 200
