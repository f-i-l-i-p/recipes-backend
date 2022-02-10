"""
API for handling recipes.
"""
import json

from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import BytesIO
from urllib.request import urlopen

from server.database import interface

recipe_api = Blueprint('recipe_api', __name__)


@recipe_api.route('/create', methods=['POST'])
@jwt_required()
def create():
    """
    Lets the logged in user create a recipe.
    """
    data = json.loads(request.data)
    name = data['name']
    ingredients = json.dumps(data['ingredients'])
    instructions = json.dumps(data['instructions'])
    image = data['image']

    user = interface.get_user_by_id(get_jwt_identity())

    interface.create_recipe(user, name, ingredients, instructions, image)

    return '', 200


@recipe_api.route('/change', methods=['POST'])
@jwt_required()
def change():
    """
    Lets the logged in user change the contents of a recipe.
    """
    data = json.loads(request.data)
    recipe_id = data['id']
    name = data['name']
    ingredients = json.dumps(data['ingredients'])
    instructions = json.dumps(data['instructions'])
    image = data['image']

    user = interface.get_user_by_id(get_jwt_identity())

    for recipe in user.recipes:
        if recipe_id == recipe.id:
            interface.change_recipe(recipe_id, name, ingredients, instructions, image)
            return '', 200

    return "Wrong recipe id", 400


@recipe_api.route('/delete', methods=['POST'])
@jwt_required()
def delete():
    """
    Lets the logged in user delete a recipe.
    """
    data = json.loads(request.data)
    recipe_id = data['id']
    user = interface.get_user_by_id(get_jwt_identity())

    for recipe in user.recipes:
        if recipe_id == recipe.id:
            interface.delete_recipe(recipe)
            return '', 200

    return "Wrong recipe id", 400


@recipe_api.route('/get', methods=['POST'])
@jwt_required()
def get():
    """
    Returns the recipe with a specified id.
    """
    data = json.loads(request.data)
    id = data['id']

    # TODO: Check if this is allowed for this user.
    recipe = interface.get_recipe_by_id(id)

    result = {'id': recipe.id,
              'name': recipe.name,
              'ingredients': json.loads(recipe.ingredients),
              'instructions': json.loads(recipe.instructions),
              'user': recipe.user.name,
              'likes': len(recipe.liked_by),
              'image': recipe.image}

    return result, 200


@recipe_api.route('/like', methods=['POST'])
@jwt_required()
def like():
    """
    Makes the logged in user like a recipe.
    """
    data = json.loads(request.data)
    recipe_id = data['id']

    recipe = interface.get_recipe_by_id(recipe_id)
    if recipe is None:
        return {'msg': 'Can\'t find recipe.'}, 400

    user = interface.get_user_by_id(get_jwt_identity())

    interface.like_recipe(user, recipe)

    return '', 200


@recipe_api.route('/unlike', methods=['POST'])
@jwt_required()
def unlike():
    """
    Makes the logged in user unlike a recipe.
    """
    data = json.loads(request.data)
    recipe_id = data['id']

    recipe = interface.get_recipe_by_id(recipe_id)
    if recipe is None:
        return {'msg': 'Can\'t find recipe.'}, 400

    user = interface.get_user_by_id(get_jwt_identity())

    interface.stop_like_recipe(user, recipe)

    return '', 200


@recipe_api.route('/is_liked', methods=['POST'])
@jwt_required()
def is_liked():
    """
    Returns whether the logged in user has liked a given recipe.
    """
    data = json.loads(request.data)
    recipe_id = data['id']

    recipe = interface.get_recipe_by_id(recipe_id)
    if recipe is None:
        return {'msg': 'Can\'t find recipe.'}, 400

    user = interface.get_user_by_id(get_jwt_identity())

    liked = recipe in user.liked_recipes

    return {'liked': liked}, 200


@recipe_api.route('/latest', methods=['POST'])
@jwt_required()
def latest():
    """
    Returns a list with the latest recipes created by the logged in user and its friends.
    If a match is given, it will only return recipes with match as a substring.
    """
    data = json.loads(request.data)

    if 'match' in data:
        match = data['match']
    else:
        match = ''

    user = interface.get_user_by_id(get_jwt_identity())

    recipe_creators = [user] + user.friends
    recipes = interface.latest_recipes(recipe_creators, match)

    result = [{'id': recipe.id, 'name': recipe.name, 'user': recipe.user.name}
              for recipe in recipes]

    return {'result': result}, 200


@recipe_api.route('/images/<int:recipe_id>')
def get_image(recipe_id):
    """
    Returns the image for a recipe.
    """
    # TODO: Check if this is allowed for this user.
    recipe = interface.get_recipe_by_id(recipe_id)

    if not (recipe and recipe.image):
        return '', 404

    with urlopen(recipe.image) as response:
        data = response.read()

    return send_file(BytesIO(data), attachment_filename=f'{recipe_id}.jpg')
