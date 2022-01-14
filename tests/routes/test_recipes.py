from datetime import date
import json
import unittest
from tests.routes.test_helpers.recipes_helper import create_recipe_image, create_recipe_ingredients, create_recipe_instructions

from tests.routes.test_helpers.route_test_case import RouteTestCase
from tests.routes.test_helpers.users_helper import create_and_login_user, create_user, login_user


class RecipesTests(RouteTestCase):
    def test_create(self):
        token = create_and_login_user(self, "user")

        name = 'the recipe' * 10000
        ingredients = 'an ingredient\n' * 10000
        instructions = 'an instruction\n' * 10000
        image = 'image as a string' * 10000

        res = self.client.post('recipes/create',
                               json={'name': name, 'ingredients': ingredients, 'instructions': instructions,
                                     'image': image},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)

    def test_change(self):
        user = create_user(self, "user")
        token = login_user(self, "user")

        old_name = "old name"
        old_ingredients = "old"
        old_instructions = "old instructions"
        old_image = "old image"
        old_recipe = self.data.create_recipe(
            user, old_name, old_ingredients, old_instructions, old_image)

        new_name = "new name"
        new_ingredients = ['new ingredient 1',
                           'new ingredient 2', 'new ingredient 3']
        new_instructions = ["new instruction 1", "new instruction 2"]
        new_image = "new image"

        res = self.client.post('recipes/change',
                               json={'id': old_recipe.id, 'name': new_name, 'ingredients': new_ingredients, 'instructions': new_instructions,
                                     'image': new_image},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        new_recipe = self.data.get_recipe_by_id(old_recipe.id)
        self.assertEqual(new_recipe.name, new_name)
        self.assertEqual(new_recipe.ingredients, json.dumps(new_ingredients))
        self.assertEqual(new_recipe.instructions, json.dumps(new_instructions))
        self.assertEqual(new_recipe.image, new_image)

    def test_delete(self):
        user = create_user(self, "user")
        token = login_user(self, "user")
        recipe = self.data.create_recipe(user, "", "", "", "")

        res = self.client.post('recipes/delete',
                               json={'id': recipe.id},
                               headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code, 200)
        user = self.data.get_user_by_name("user")
        self.assertEqual(user.recipes, [])

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
