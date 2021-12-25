"""
API for handling friendships.
"""
import json

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.database import interface

friend_api = Blueprint('friend_api', __name__)


@friend_api.route('/create-friend-request', methods=['POST'])
@jwt_required()
def create_friend_request():
    """
    Creates a new friend request.
    """
    data = json.loads(request.data)
    friend_id = data['id']

    user = interface.get_user_by_id(get_jwt_identity())
    friend = interface.get_user_by_id(friend_id)

    interface.create_friend_request(user, friend)

    return '', 200


@friend_api.route('/cancel-friend-request', methods=['POST'])
@jwt_required()
def cancel_friend_request():
    """
    Cancels an existing friend request.
    """
    data = json.loads(request.data)
    friend_id = data['id']

    user = interface.get_user_by_id(get_jwt_identity())
    friend = interface.get_user_by_id(friend_id)

    interface.cancel_friend_request(user, friend)

    return '', 200


@friend_api.route('/accept-friend-request', methods=['POST'])
@jwt_required()
def accept_friend_request():
    """
    Accepts an existing friend request.
    """
    data = json.loads(request.data)
    friend_id = data['id']

    user = interface.get_user_by_id(get_jwt_identity())
    friend = interface.get_user_by_id(friend_id)

    interface.accept_friend_request(user, friend)

    return '', 200


@friend_api.route('/remove-friend', methods=['POST'])
@jwt_required()
def remove_friend():
    """
    Accepts an existing friend request.
    """
    data = json.loads(request.data)
    friend_id = data['id']

    user = interface.get_user_by_id(get_jwt_identity())
    friend = interface.get_user_by_id(friend_id)

    interface.remove_friendship(user, friend)

    return '', 200
