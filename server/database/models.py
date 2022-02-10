from server.database.handler import db
from typing import Dict


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False)


liked_recipes_table = db.Table(
    'liked_recipes_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
)

friendship = db.Table(
    'friendships',
    db.Column('user1_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('user2_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

friendship_request = db.Table(
    'friendship_requests',
    db.Column('requesting_user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('receiving_user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    pw_hash = db.Column(db.String, nullable=False)

    friends = db.relationship(
        'User',
        secondary=friendship,
        primaryjoin=id == friendship.c.user1_id,
        secondaryjoin=id == friendship.c.user2_id
    )

    outgoing_friend_requests = db.relationship(
        'User',
        secondary=friendship_request,
        primaryjoin=id == friendship_request.c.requesting_user_id,
        secondaryjoin=id == friendship_request.c.receiving_user_id,
        backref='incoming_friend_requests'
    )

    liked_recipes = db.relationship(
        'Recipe',
        secondary=liked_recipes_table,
        back_populates='liked_by'
    )

    recipes = db.relationship("Recipe")

    def get_public_data(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
        }


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)
    instructions = db.Column(db.String)
    image = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="recipes")

    liked_by = db.relationship(
        'User',
        secondary=liked_recipes_table,
        back_populates='liked_recipes'
    )
