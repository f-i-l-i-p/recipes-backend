"""
API for handling following.
"""
import json

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.database import interface

follow_api = Blueprint('follow_api', __name__)


@follow_api.route('/following', methods=['POST'])
@jwt_required()
def following():
    """
    Returns a list with all the users the the logged in user is following.
    """
    user = interface.get_user_by_id(get_jwt_identity())

    result = [followed.name for followed in user.following]

    return {'result': result}, 200


@follow_api.route('/follow', methods=['POST'])
@jwt_required()
def follow():
    """
    Makes the logged in user follow another user.
    """
    data = json.loads(request.data)

    to_follow = interface.get_user_by_name(data['follow'])
    user = interface.get_user_by_id(get_jwt_identity())

    interface.follow_user(user, to_follow)

    return '', 200


@follow_api.route('/unfollow', methods=['POST'])
@jwt_required()
def unfollow():
    """
    Makes the logged in user unfollow another user.
    """
    data = json.loads(request.data)

    to_unfollow = interface.get_user_by_name(data['unfollow'])
    user = interface.get_user_by_id(get_jwt_identity())

    interface.unfollow_user(user, to_unfollow)

    return '', 200
