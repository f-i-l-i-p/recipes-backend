import unittest

from tests.routes.test_helpers.requests import create_and_log_in_user, create_user
from tests.routes.test_helpers.route_test_case import RouteTestCase


class FollowTests(RouteTestCase):
    def test_following(self):
        token = create_and_log_in_user(self.client, 'user1')
        create_user(self.client, 'user2')

        res = self.client.post('follow/following', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.json['result'], [])

        self.client.post('follow/follow', json={'follow': 'user2'},
                         headers={'Authorization': f'Bearer {token}'})

        res = self.client.post('follow/following', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.json['result'], ['user2'])

    def test_follow(self):
        token = create_and_log_in_user(self.client, 'user1')
        create_user(self.client, 'user2')

        res = self.client.post('follow/follow', json={'follow': 'user2'},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

    def test_unfollow(self):
        token = create_and_log_in_user(self.client, 'user1')
        create_user(self.client, 'user2')

        res = self.client.post('follow/unfollow', json={'unfollow': 'user2'},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

        self.client.post('follow/follow', json={'follow': 'user2'},
                         headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

        res = self.client.post('follow/unfollow', json={'unfollow': 'user2'},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

        res = self.client.post('follow/following', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.json['result'], [])


if __name__ == '__main__':
    unittest.main()
