import json
from tests.routes.test_helpers.route_test_case import RouteTestCase
from server.database.models import Recipe, User


def create_recipe_ingredients():
    ingredients = [{
        "name": "test",
        "unit": "kg",
        "quantity": 4
    }] * 100

    return json.dumps(ingredients)


def create_recipe_instructions():
    instructions = ["instruction"] * 100

    return json.dumps(instructions)


def create_recipe_image():
    # this is not an image, just some random characters
    return "AKDHFAKJDFALJDFLKAFLKAJDKLASDJHFJDJFFLKADJLAKFDSJLKADSJLKDSAJFLKAJ"
