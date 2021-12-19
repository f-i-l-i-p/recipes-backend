"""
Functions for interacting with the database.
"""
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import and_, func

from server.database.handler import db
from server.database.models import User, Recipe, Comment, TokenBlocklist


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

def create_user(user_name: str, pw_hash: str) -> User:
    """
    Creates a new user and adds it to the database.
    :return: The new user.
    """
    user = User(name=user_name, pw_hash=pw_hash)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_name(user_name: str) -> Optional[User]:
    """
    Returns the user with a given name if it exists.
    :return: User object or none.
    """
    user = User.query.filter_by(name=user_name).first()

    return user


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Returns the user with a given id if it exists.
    :return: User object or none.
    """
    user = User.query.filter_by(id=user_id).first()

    return user


def search_users(match: str) -> List[User]:
    """
    Returns all users that has ´match´ as a substring in the username.
    :return: List with User objects.
    """
    users = User.query.filter(func.lower(User.name).contains(match.lower())).all()

    return users


# ============================================================================
# FOLLOWING
# ============================================================================

def follow_user(user: User, user_to_follow: User) -> None:
    """
    Makes a user follow another.
    """
    if user_to_follow in user.following:
        return

    user.following.append(user_to_follow)
    db.session.commit()


def unfollow_user(user: User, user_to_unfollow: User) -> None:
    """
    Makes a user unfollow another.
    """
    if user_to_unfollow not in user.following:
        return

    user.following.remove(user_to_unfollow)
    db.session.commit()


# ============================================================================
# COMMENTS
# ============================================================================

def create_comment(user: User, recipe: Recipe, text: str) -> Comment:
    """
    Creates a new comment.
    :param user: User who commented.
    :param recipe: Recipe that the comment is for.
    :param text: Comment text.
    :return: A comment object.
    """
    comment = Comment(user_id=user.id, recipe_id=recipe.id,
                      text=text, date=datetime.now(timezone.utc))

    db.session.add(comment)
    db.session.commit()

    return comment


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
    recipes = Recipe.query.filter(func.lower(Recipe.name).contains(match.lower())).all()

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

    recipes = Recipe.query.filter(and_(Recipe.id.in_(recipe_ids),
                                       func.lower(Recipe.name).contains(match.lower()))). \
        order_by(Recipe.id.desc()). \
        all()

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
