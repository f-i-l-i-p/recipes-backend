import unittest

from server.database import handler
from server.main import app
from server.database.handler import db
from server.database import handler, interface


class RouteTestCase(unittest.TestCase):
    data = interface

    def setUp(self):
        app.config['TESTING'] = True
        app.app_context().push()
        handler.init_db(app)
        self.client = app.test_client()
        db.session.close()
