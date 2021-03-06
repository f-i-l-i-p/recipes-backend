"""
Functions for interacting with the database.
"""
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import and_, func

from server.database.handler import db
from server.database.models import User, Recipe, TokenBlocklist


# ============================================================================
# TOKENS
# ============================================================================

def revoke_token(jti: str) -> None:
    """
    Revokes a given token.
    """
    b = TokenBlocklist(jti=jti, revoked_at=datetime.now(timezone.utc))

    db.session.add(b)
    db.session.commit()


def is_revoked(jti: str) -> bool:
    """
    Returns True if a given token is revoked.
    """
    b = TokenBlocklist.query.filter_by(jti=jti).first()

    return b is not None


# ============================================================================
# USERS
# ============================================================================

def create_user(user_name: str, user_email: str, pw_hash: str) -> User:
    """
    Creates a new user and adds it to the database.
    :return: The new user.
    """
    user = User(name=user_name, email=user_email, pw_hash=pw_hash)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Returns the user with a given id if it exists.
    :return: User object or none.
    """
    user = User.query.filter_by(id=user_id).first()

    return user


def get_user_by_email(user_email: str) -> Optional[User]:
    """
    Returns the user with a given email if it exists.
    :return: User object or none.
    """
    user = User.query.filter_by(email=user_email).first()

    return user


def search_users(match: str) -> List[User]:
    """
    Returns all users that has ´match´ as a substring in the username.
    :return: List with User objects.
    """
    users = User.query.filter(func.lower(
        User.name).contains(match.lower())).all()

    return users


# ============================================================================
# FRIENDS
# ============================================================================

def create_friend_request(sender: User, receiver: User) -> None:
    """
    Creates a new friend request.
    :param sender: User who sends the request.
    :param receiver: User who should receve the request.
    """
    sender.outgoing_friend_requests.append(receiver)
    db.session.commit()


def cancel_friend_request(user1: User, user2: User) -> None:
    """
    Cancels friend requests between two users.
    """
    if (user2 in user1.outgoing_friend_requests):
        user1.outgoing_friend_requests.remove(user2)
        db.session.commit()
    elif (user1 in user2.outgoing_friend_requests):
        user2.outgoing_friend_requests.remove(user1)
        db.session.commit()


def accept_friend_request(user1: User, user2: User) -> None:
    """
    Accepts a friend request between two users.
    """
    cancel_friend_request(user1, user2)

    if (user2 not in user1.friends):
        user1.friends.append(user2)
        user2.friends.append(user1)
        db.session.commit()


def remove_friendship(user1: User, user2: User) -> None:
    """
    Removes friendship between two users.
    """
    if (user2 in user1.friends):
        user1.friends.remove(user2)
        user2.friends.remove(user1)
        db.session.commit()


# ============================================================================
# RECIPES
# ============================================================================

def create_recipe(user: User, name: str, ingredients: str, instructions: str, image: str) -> Recipe:
    """
    Creates a new recipe.
    :param user: User who created the recipe.
    :param name: Recipe name.
    :param ingredients: Recipe ingredients.
    :param instructions: Recipe instructions.
    :return: The new recipe.
    """
    recipe = Recipe(name=name, ingredients=ingredients,
                    instructions=instructions, image=image, user_id=user.id)

    db.session.add(recipe)
    db.session.commit()

    return recipe


def change_recipe(recipe_id: int, new_name: str, new_ingredients: str, new_instructions: str, new_image: str) -> None:
    """
    Updates an existing recipe. Empty or None values will is ignored.
    """
    recipe = get_recipe_by_id(recipe_id)

    if not recipe: return

    if new_name: recipe.name = new_name
    if new_ingredients: recipe.ingredients = new_ingredients
    if new_instructions: recipe.instructions = new_instructions
    if new_image: recipe.image = new_image

    db.session.commit()


def delete_recipe(recipe: Recipe) -> None:
    """
    Deletes a given recipe.
    """
    db.session.delete(recipe)
    db.session.commit()


def get_recipe_by_id(recipe_id: int) -> Optional[Recipe]:
    """
    Returns the recipe with a given id if it exists.
    :return: Recipe object or none.
    """
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    return recipe


def search_recipes(match: str) -> List[Recipe]:
    """
    Returns all recipes that has ´match´ as a substring in the recipe name.
    :return: List with Recipe objects.
    """
    recipes = Recipe.query.filter(func.lower(
        Recipe.name).contains(match.lower())).all()

    return recipes


def latest_recipes(users: List[User], match: str) -> List[Recipe]:
    """
    Returns all recipes that is created by one of the given users
    and has ´match´ as a substring in the recipe name.
    The recipes will be sorted by last created (highest id).
    :return: List with Recipe objects.
    """
    recipe_ids = []
    for user in users:
        for recipe in user.recipes:
            recipe_ids.append(recipe.id)

    recipes = Recipe.query.filter(and_(Recipe.id.in_(recipe_ids), func.lower(
        Recipe.name).contains(match.lower()))).order_by(Recipe.id.desc()).all()

    return recipes


# ============================================================================
# LIKES
# ============================================================================

def like_recipe(user: User, recipe: Recipe) -> None:
    """
    Makes a user like a recipe.
    """
    if recipe in user.liked_recipes:
        return

    user.liked_recipes.append(recipe)
    db.session.commit()


def stop_like_recipe(user: User, recipe: Recipe) -> None:
    """
    Makes a user stop liking a recipe.
    """
    if recipe not in user.liked_recipes:
        return

    user.liked_recipes.remove(recipe)
    db.session.commit()
