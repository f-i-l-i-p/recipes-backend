import unittest
from tests.routes.test_helpers.recipes_helper import create_recipe_image, create_recipe_ingredients, create_recipe_instructions

from tests.routes.test_helpers.requests import create_and_log_in_user
from tests.routes.test_helpers.route_test_case import RouteTestCase
from tests.routes.test_helpers.users_helper import create_user, login_user


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
        user = create_user(self, "user")
        token = login_user(self, "user")

        name = "recipe name"
        ingredients = create_recipe_ingredients()
        instructions = create_recipe_instructions()
        image = create_recipe_image()

        self.data.create_recipe(user, name, ingredients, instructions, image)

        res = self.client.post('recipes/get', json={"id": 1},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
