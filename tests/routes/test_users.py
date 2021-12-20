import unittest

from tests.routes.test_helpers.requests import create_user, log_in_user
from tests.routes.test_helpers.route_test_case import RouteTestCase


class UsersTests(RouteTestCase):
    def test_create_user(self):
        res = self.client.post('users/create', json={'user_name': 'user1', 'email': 'test@test.test', 'password': '1234'})
        self.assertEqual(res.status_code, 200)

        res = self.client.post('users/create', json={'user_name': 'user2', 'email': 'test@test.test', 'password': '5678'})
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json, {'msg': 'Email already in use'})

    def test_search(self):
        user_names = ["test0", "test1", "test2"]
        for name in user_names:
            create_user(self.client, name, name + '@test.test', "1234")

        token = log_in_user(self.client, "test0@test.test", "1234")

        res = self.client.post('users/search', json={'search_term': 's'}, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'result': [{"name": "test1", "following": False}, {"name": "test2", "following": False}]})


if __name__ == '__main__':
    unittest.main()
