import unittest

from tests.routes.test_helpers.route_test_case import RouteTestCase


class AuthTests(RouteTestCase):
    def test_login(self):
        name, email, pwd = 'user1', 'test@test.test', '1234'
        self.client.post('users/create', json={'user_name': name, 'email': email, 'password': pwd})

        res = self.client.post('auth/login', json={ 'email': 'wrong', 'password': pwd})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json, {'msg': 'Wrong email or password'})

        res = self.client.post('auth/login', json={ 'email': email, 'password': 'wrong'})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json, {'msg': 'Wrong email or password'})

        res = self.client.post('auth/login', json={ 'email': email, 'password': pwd})
        self.assertEqual(res.status_code, 200)
        self.assertTrue('token' in res.json.keys())

        # Check logged in
        token = res.json['token']
        res = self.client.post('auth/check', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'msg': 'Access'})

    def test_logout(self):
        name, email, pwd = 'user1', 'test@test.test', '1234'
        self.client.post('users/create', json={'user_name': name, 'email': email, 'password': pwd})
        token = self.client.post('auth/login', json={'email': email, 'password': pwd}).json['token']

        # Check logged in
        res = self.client.post('auth/check', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'msg': 'Access'})

        # Log out
        res = self.client.post('auth/logout', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'msg': 'Access token revoked'})

        # Check not logged in
        res = self.client.post('auth/check', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json, {'msg': 'Token has been revoked'})

    def test_check(self):
        res = self.client.post('auth/check')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json, {'msg': 'Missing Authorization Header'})


if __name__ == '__main__':
    unittest.main()
