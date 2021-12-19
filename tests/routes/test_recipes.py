import unittest

from tests.routes.test_helpers.requests import create_and_log_in_user, create_recipe
from tests.routes.test_helpers.route_test_case import RouteTestCase


class RecipesTests(RouteTestCase):
    def test_create(self):
        token = create_and_log_in_user(self.client)

        name = 'the recipe' * 10000
        ingredients = 'an ingredient\n' * 10000
        instructions = 'an instruction\n' * 10000
        image = 'image as a string' * 10000

        res = self.client.post('recipes/create',
                               json={'name': name, 'ingredients': ingredients, 'instructions': instructions,
                                     'image': image},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)

    def test_get(self):
        token = create_and_log_in_user(self.client, "user")
        create_recipe(self.client, token, "recipe0")
        create_recipe(self.client, token, "recipe1")
        create_recipe(self.client, token, "abcd")
        create_recipe(self.client, token, "recipe2")

        res = self.client.post('recipes/latest', json={'match': 'cipe'},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.json['result'], [{'id': 4, 'name': 'recipe2', 'user': 'user'},
                                              {'id': 2, 'name': 'recipe1', 'user': 'user'},
                                              {'id': 1, 'name': 'recipe0', 'user': 'user'}])

        if __name__ == '__main__':
            unittest.main()
