import unittest

from tests.routes.test_helpers.route_test_case import RouteTestCase
from tests.routes.test_helpers.users_helper import create_user, login_user


class FriendsTests(RouteTestCase):
    def test_list_friends(self):
        user1 = create_user(self, 'user1')
        user2 = create_user(self, 'user2')
        user3 = create_user(self, 'user3')
        user4 = create_user(self, 'user4')
        token = login_user(self, 'user1')

        res = self.client.post('friends/list-friends',
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {
            "friends": [],
            "outgoing_requests": [],
            "incoming_requests": []
        })

        self.data.create_friend_request(user1, user2)
        self.data.accept_friend_request(user1, user2)
        self.data.create_friend_request(user1, user3)
        self.data.create_friend_request(user4, user1)

        res = self.client.post('friends/list-friends',
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {
            "friends": [user2.get_public_data()],
            "outgoing_requests": [user3.get_public_data()],
            "incoming_requests": [user4.get_public_data()]
        })

    def test_create_friend_request(self):
        user1 = create_user(self, 'user1')
        user2 = create_user(self, 'user2')
        token = login_user(self, 'user1')

        res = self.client.post('friends/create-friend-request',
                               json={'id': user2.id},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(user1.outgoing_friend_requests, [user2])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [user1])

    def test_cancel_friend_request(self):
        user1 = create_user(self, 'user1')
        user2 = create_user(self, 'user2')
        self.data.create_friend_request(user1, user2)
        token = login_user(self, 'user1')

        res = self.client.post('friends/cancel-friend-request',
                               json={'id': user2.id},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(user1.outgoing_friend_requests, [])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [])

    def test_accept_friend_request(self):
        user1 = create_user(self, 'user1')
        user2 = create_user(self, 'user2')
        self.data.create_friend_request(user1, user2)
        token = login_user(self, 'user1')

        res = self.client.post('friends/accept-friend-request',
                               json={'id': user2.id},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(user1.friends, [user2])
        self.assertEqual(user2.friends, [user1])

    def test_remove_friend(self):
        user1 = create_user(self, 'user1')
        user2 = create_user(self, 'user2')
        self.data.create_friend_request(user1, user2)
        self.data.accept_friend_request(user1, user2)
        token = login_user(self, 'user1')

        res = self.client.post('friends/remove-friend',
                               json={'id': user2.id},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(user1.friends, [])
        self.assertEqual(user2.friends, [])


if __name__ == '__main__':
    unittest.main()
