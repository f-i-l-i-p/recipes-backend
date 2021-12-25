from tests.routes.test_helpers.route_test_case import RouteTestCase
from server.database.models import User


def create_user(test: RouteTestCase, name: str) -> User:
    email, pw = _get_email_and_pw(name)

    test.client.post('users/create', json={'user_name': name, 'email': email, 'password': pw})
    return test.data.get_user_by_name(name)


def login_user(test: RouteTestCase, name: str) -> int:
    email, pw = _get_email_and_pw(name)

    res = test.client.post('auth/login', json={'email': email, 'password': pw})
    return res.json['token']


def create_and_login_user(test: RouteTestCase, name: str) -> int:
    create_user(test, name)
    return login_user(test, name)


def _get_email_and_pw(name: str):
    return name + "@example.com", "password"
