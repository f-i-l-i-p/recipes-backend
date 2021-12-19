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
    password = data['password']

    if interface.get_user_by_name(user_name):
        return {'msg': "Username already taken"}, 409

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    interface.create_user(user_name, password_hash)

    return '', 200


@user_api.route('/search', methods=['POST'])
@jwt_required()
def search():
    """
    Searches for users with their name.
    Returns a list with dicts containing the keys ´name´ and ´following´.
    """
    data = json.loads(request.data)

    search_term = data['search_term']
    this_user = interface.get_user_by_id(get_jwt_identity())

    users = interface.search_users(search_term)

    result = []
    for user in users:
        if user.name == this_user.name:
            continue
        elif user in this_user.following:
            result.append({'name': user.name, 'following': True})
        else:
            result.append({'name': user.name, 'following': False})

    return {'result': result}, 200

