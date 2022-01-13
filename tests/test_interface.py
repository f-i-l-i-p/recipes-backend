import unittest
from server.database import handler, interface
from server.database.handler import db
from server.database.models import User
from server.main import app


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        app.app_context().push()
        handler.init_db(app)
        db.session.close()

    # ============================================================================
    # USERS
    # ============================================================================

    def test_create_user(self):
        name = "this is a long name with weird characters Ä#¶[$¤½?';{£ħœ|"
        user = interface.create_user(name, "email@test.test", "1234")

        self.assertEqual(type(user), User, "Incorrect return type")
        self.assertEqual(user.name, name), "Incorrect name"
        self.assertEqual(user.pw_hash, "1234"), "Incorrect pw hash"
        self.assertEqual(user.outgoing_friend_requests, [])
        self.assertEqual(user.incoming_friend_requests, [])
        self.assertEqual(user.comments, [])
        self.assertEqual(user.recipes, [])

    def test_get_user_by_name(self):
        name = "this is a long name with weird characters Ä#¶[$¤½?';{£ħœ|"
        user1 = interface.create_user(name, "email@test.test", "1234")
        user2 = interface.get_user_by_name(name)
        
        self.assertEqual(user1, user2, "Returned wrong user")
        self.assertIsNone(interface.get_user_by_name("Wrong_name"), "Should return None")

    def test_get_user_by_email(self):
        user1 = interface.create_user("name", "email@test.test", "1234")
        user2 = interface.get_user_by_name("name")

        self.assertEqual(user1, user2, "Returned wrong user")
        self.assertIsNone(interface.get_user_by_name("Wrong_name"), "Should return None")

    def test_get_user_by_id(self):
        user1 = interface.create_user("filip", "email@test.test", "1234")
        user2 = interface.get_user_by_id(user1.id)

        self.assertEqual(user1, user2, "Returned wrong user")
        self.assertIsNone(interface.get_user_by_id(999999), "Should return None")

    def test_search_users(self):
        names = ["user1", "user2", "user3", "£$€¥¡@]", "test1", "test2"]
        for name in names:
            interface.create_user(name, name + "@test.test", "password")

        users = interface.search_users("no")
        self.assertEqual(users, [])

        users = interface.search_users("sEr")
        self.assertEqual([user.name for user in users], ["user1", "user2", "user3"])

        users = interface.search_users("uSeR3")
        self.assertEqual([user.name for user in users], ["user3"])

        users = interface.search_users("¥¡")
        self.assertEqual([user.name for user in users], ["£$€¥¡@]"])

        users = interface.search_users("")
        self.assertEqual([user.name for user in users], ["user1", "user2", "user3", "£$€¥¡@]", "test1", "test2"])

    # ============================================================================
    # FRIENDS
    # ============================================================================

    def test_create_friend_request(self):
        user1 = interface.create_user("user1", "user1@test.test", "password")
        user2 = interface.create_user("user2", "user2@test.test", "password")

        interface.create_friend_request(user1, user2)

        self.assertEqual(user1.outgoing_friend_requests, [user2])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [user1])

    def test_cancel_friend_request(self):
        user1 = interface.create_user("user1", "user1@test.test", "password")
        user2 = interface.create_user("user2", "user2@test.test", "password")

        interface.create_friend_request(user1, user2)
        interface.cancel_friend_request(user1, user2)

        self.assertEqual(user1.outgoing_friend_requests, [])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [])

        interface.create_friend_request(user1, user2)
        interface.cancel_friend_request(user2, user1)

        self.assertEqual(user1.outgoing_friend_requests, [])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [])

    def test_accept_friend_request(self):
        user1 = interface.create_user("user1", "user1@test.test", "password")
        user2 = interface.create_user("user2", "user2@test.test", "password")
        user3 = interface.create_user("user3", "user3@test.test", "password")
        interface.create_friend_request(user1, user2)
        interface.create_friend_request(user1, user3)

        interface.accept_friend_request(user1, user2)
        interface.accept_friend_request(user3, user1)

        self.assertEqual(user1.outgoing_friend_requests, [])
        self.assertEqual(user1.incoming_friend_requests, [])
        self.assertEqual(user1.friends, [user2, user3])
        self.assertEqual(user2.outgoing_friend_requests, [])
        self.assertEqual(user2.incoming_friend_requests, [])
        self.assertEqual(user2.friends, [user1])
        self.assertEqual(user3.outgoing_friend_requests, [])
        self.assertEqual(user3.incoming_friend_requests, [])
        self.assertEqual(user3.friends, [user1])

    def test_remove_friendship(self):
        user1 = interface.create_user("user1", "user1@test.test", "password")
        user2 = interface.create_user("user2", "user2@test.test", "password")
        user3 = interface.create_user("user3", "user3@test.test", "password")
        interface.create_friend_request(user1, user2)
        interface.create_friend_request(user1, user3)
        interface.accept_friend_request(user1, user2)
        interface.accept_friend_request(user1, user3)

        interface.remove_friendship(user1, user2)
        interface.remove_friendship(user3, user1)

        self.assertEqual(user1.friends, [])
        self.assertEqual(user2.friends, [])
        self.assertEqual(user3.friends, [])

    # ============================================================================
    # COMMENTS
    # ============================================================================

    def test_create_comment(self):
        user = interface.create_user("user", "email@test.test", "pw")
        recipe = interface.create_recipe(user, "recipe", "ingredients", "instructions", "image")

        comment1 = interface.create_comment(user, recipe, "hello")
        comment2 = interface.create_comment(user, recipe, "hello again")

        self.assertEqual(comment1.user, user)
        self.assertEqual(comment1.recipe, recipe)
        self.assertEqual(user.comments, [comment1, comment2])
        self.assertEqual(recipe.comments, [comment1, comment2])

    # ============================================================================
    # RECIPES
    # ============================================================================

    def test_create_recipe(self):
        user = interface.create_user("user", "email@test.test", "pw")
        name = "Recipe" * 100
        ingredients = "Ingredient\n" * 10000
        instructions = "Instruction\n" * 10000
        image = "image in string format" * 10000

        recipe = interface.create_recipe(user, name, ingredients, instructions, image)
        self.assertIsNotNone(recipe)
        self.assertIsNotNone(recipe.user)
        self.assertEqual(recipe.name, name)
        self.assertEqual(recipe.ingredients, ingredients)
        self.assertEqual(recipe.instructions, instructions)
        self.assertEqual(recipe.image, image)
        self.assertEqual(recipe.comments, [])
        self.assertEqual(user.recipes, [recipe])

    def test_change_recipe(self):
        user = interface.create_user("user", "user@example.com", "pw")
        name = "old name"
        ingredients = "old ingredients"
        instructions = "old instructions"
        image = "old image"
        recipe = interface.create_recipe(user, name, ingredients, instructions, image)
        
        new_name = "new name"
        new_ingredients = "new ingredients"
        new_instructions = "new instructions"
        new_image = "new image"
        interface.change_recipe(recipe.id, new_name, new_ingredients, new_instructions, new_image)

        new_recipe = interface.get_recipe_by_id(recipe.id)
        self.assertEqual(recipe.id, new_recipe.id)
        self.assertEqual(new_recipe.user, user)
        self.assertEqual(new_recipe.name, new_name)
        self.assertEqual(new_recipe.ingredients, new_ingredients)
        self.assertEqual(new_recipe.instructions, new_instructions)
        self.assertEqual(new_recipe.image, new_image)

    def test_search_recipes(self):
        user = interface.create_user("user", "email@test.test", "pw")
        recipe_names = ["recipe1", "recipe2", "recipe3", "£@$£@$€", "test1", "test2"]
        for name in recipe_names:
            interface.create_recipe(user, name, "ingredients", "instructions", "image")

        recipes = interface.search_recipes("no")
        self.assertEqual(recipes, [])

        recipes = interface.search_recipes("ciP")
        self.assertEqual([recipe.name for recipe in recipes], ["recipe1", "recipe2", "recipe3"])

        recipes = interface.search_recipes("rEcIpE3")
        self.assertEqual([recipe.name for recipe in recipes], ["recipe3"])

        recipes = interface.search_recipes("@$£")
        self.assertEqual([recipe.name for recipe in recipes], ["£@$£@$€"])

        recipes = interface.search_recipes("")
        self.assertEqual([recipe.name for recipe in recipes],
                         ["recipe1", "recipe2", "recipe3", "£@$£@$€", "test1", "test2"])

    def test_latest_recipes(self):
        user_names = ["user1", "user2", "user3"]
        users = [interface.create_user(user_name, user_name + "@test.test", "1234") for user_name in user_names]
        recipe_names = ["recipe1", "recipe2", "recipe3", "recipe4", "recipe5"]
        recipes = []

        for index, recipe_name in enumerate(recipe_names):
            recipes.append(
                interface.create_recipe(users[index % len(users)], recipe_name, "ingredients", "instructions", "image"))

        latest = interface.latest_recipes(users, '')
        self.assertEqual(latest, recipes[::-1])

        latest = interface.latest_recipes([users[1]], '')
        self.assertEqual(latest, [recipes[4], recipes[1]])

        latest = interface.latest_recipes(users, 'iPE')
        self.assertEqual(latest, recipes[::-1])

        latest = interface.latest_recipes(users, 'iPe3')
        self.assertEqual(latest, [recipes[2]])

        latest = interface.latest_recipes([users[1]], 'kaldjhjhjhgytfvgguyga')
        self.assertEqual(latest, [])

        latest = interface.latest_recipes([], '')
        self.assertEqual(latest, [])

    # ============================================================================
    # LIKES
    # ============================================================================

    def test_like_recipe(self):
        user_names = ["user0", "user1", "user2"]
        users = [interface.create_user(user_name, user_name + "@test.test", "1234") for user_name in user_names]
        recipe_names = ["recipe0", "recipe1", "recipe2", "recipe3", "recipe4"]
        recipes = []

        for index, recipe_name in enumerate(recipe_names):
            recipes.append(
                interface.create_recipe(users[index % len(users)], recipe_name, "ingredients", "instructions", "image"))

        self.assertEqual(users[0].liked_recipes, [])
        self.assertEqual(recipes[0].liked_by, [])

        # user0 like recipe0
        interface.like_recipe(users[0], recipes[0])
        self.assertEqual(recipes[0].liked_by, [users[0]])
        self.assertEqual(users[0].liked_recipes, [recipes[0]])

        # user2 like recipe0 many times
        interface.like_recipe(users[2], recipes[0])
        interface.like_recipe(users[2], recipes[0])
        interface.like_recipe(users[2], recipes[0])
        self.assertEqual(recipes[0].liked_by, [users[0], users[2]])
        self.assertEqual(users[0].liked_recipes, [recipes[0]])
        self.assertEqual(users[2].liked_recipes, [recipes[0]])

    def test_stop_like_recipe(self):
        user_names = ["user0", "user1", "user2"]
        users = [interface.create_user(user_name, user_name + "@test.test", "1234") for user_name in user_names]
        recipe_names = ["recipe0", "recipe1", "recipe2", "recipe3", "recipe4"]
        recipes = []

        for index, recipe_name in enumerate(recipe_names):
            recipes.append(
                interface.create_recipe(users[index % len(users)], recipe_name, "ingredients", "instructions", "image"))

        interface.like_recipe(users[0], recipes[0])
        interface.like_recipe(users[2], recipes[0])

        # user2 stop like recipe0
        interface.stop_like_recipe(users[2], recipes[0])
        self.assertEqual(recipes[0].liked_by, [users[0]])
        self.assertEqual(users[0].liked_recipes, [recipes[0]])
        self.assertEqual(users[2].liked_recipes, [])

        # user2 stop like recipe0 again
        interface.stop_like_recipe(users[2], recipes[0])
        self.assertEqual(recipes[0].liked_by, [users[0]])


if __name__ == '__main__':
    unittest.main()
