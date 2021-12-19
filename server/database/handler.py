import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


if 'NAMESPACE' in os.environ and os.environ['NAMESPACE'] == 'heroku':
    MODE = "heroku"
else:
    MODE = "local"


db = SQLAlchemy()


def init_db(app: Flask) -> None:
    """
    Initializes the database.
    """
    db.drop_all(app=app)
    db.create_all(app=app)


def get_db_uri() -> str:
    """
    Returns the database uri
    """
    if MODE == "local":  # when running locally: use sqlite
        db_path = os.path.join(os.path.dirname(__file__), 'db.db')
        return 'sqlite:///{}'.format(db_path)
    elif MODE == "heroku":
        return os.environ['DATABASE_URL']
    else:
        raise RuntimeError(f"Mode {MODE} is not supported.")
