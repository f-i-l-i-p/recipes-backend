from enum import unique
from server.database.handler import db


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False)


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('following_id', db.Integer, db.ForeignKey('users.id')))

liked_recipes_table = db.Table('liked_recipes_table',
                               db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                               db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    pw_hash = db.Column(db.String, nullable=False)

    following = db.relationship('User',
                                secondary=followers,
                                primaryjoin=id == followers.c.follower_id,
                                secondaryjoin=id == followers.c.following_id)

    liked_recipes = db.relationship('Recipe',
                                    secondary=liked_recipes_table,
                                    back_populates='liked_by')

    comments = db.relationship("Comment")
    recipes = db.relationship("Recipe")


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="comments")

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipe = db.relationship("Recipe", back_populates="comments")


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)
    instructions = db.Column(db.String)
    image = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="recipes")

    comments = db.relationship("Comment", back_populates="recipe")

    liked_by = db.relationship('User',
                               secondary=liked_recipes_table,
                               back_populates='liked_recipes')
