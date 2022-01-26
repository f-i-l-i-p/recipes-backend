import unittest

from tests.routes.test_helpers.route_test_case import RouteTestCase
from tests.routes.test_helpers.users_helper import create_user, login_user


class UsersTests(RouteTestCase):
    def test_create_user(self):
        res = self.client.post(
            'users/create', json={'user_name': 'user1', 'email': 'test@test.test', 'password': '1234'})
        self.assertEqual(res.status_code, 200)

        res = self.client.post(
            'users/create', json={'user_name': 'user2', 'email': 'test@test.test', 'password': '5678'})
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json, {'msg': 'Email already in use'})

    def test_search(self):
        user1 = create_user(self, "user1")
        user2 = create_user(self, "user2")
        user3 = create_user(self, "user3")
        user4 = create_user(self, "user4")
        token = login_user(self, "user1")

        res = self.client.post(
            "users/search", json={"search_term": "askdjfgj"}, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {"result": []})

        res = self.client.post(
            "users/search", json={"search_term": "ser"}, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {"result": [
            user2.get_public_data(),
            user3.get_public_data(),
            user4.get_public_data()
        ]})


if __name__ == '__main__':
    unittest.main()
