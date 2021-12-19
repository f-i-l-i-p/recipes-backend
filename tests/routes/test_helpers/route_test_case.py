import unittest

from server.database import handler
from server.main import app


class RouteTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        handler.init_db(app)
        self.client = app.test_client()
