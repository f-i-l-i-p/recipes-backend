import datetime
import os

from flask import Flask

from server.database import handler
from server.routes.auth import auth_api, bcrypt, jwt
from server.routes.friends import friend_api
from server.routes.recipes import recipe_api
from server.routes.users import user_api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = handler.get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['SERVER_SECRET']
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(weeks=1)

app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(recipe_api, url_prefix='/recipes')
app.register_blueprint(friend_api, url_prefix='/friends')
app.register_blueprint(user_api, url_prefix='/users')

handler.db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


def init():
    handler.init_db(app)


if __name__ == "__main__":
    app.debug = True
    init()
    app.run(port=5000)
