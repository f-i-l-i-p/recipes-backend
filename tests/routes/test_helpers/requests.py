"""
Helper functions for making requests.
"""


def create_and_log_in_user(client, user_name='user1', email='test@test.test', user_pw='1234') -> str:
    create_user(client, user_name, email, user_pw)
    return log_in_user(client, email, user_pw)


def create_user(client, user_name='user1', email='test@test.test', user_pw='1234') -> None:
    client.post('users/create', json={'user_name': user_name, 'email': email, 'password': user_pw})


def log_in_user(client, email, user_pw) -> str:
    res = client.post('auth/login', json={'email': email, 'password': user_pw})
    return res.json['token']


def create_recipe(client, token, recipe_name='recipe', recipe_ingredients='an ingredient\n' * 100,
                  recipe_instructions='an instruction\n' * 100, recipe_image='image' * 10000) -> None:
    client.post('recipes/create',
                json={'name': recipe_name, 'ingredients': recipe_ingredients,
                      'instructions': recipe_instructions, 'image': recipe_image},
                headers={'Authorization': f'Bearer {token}'})
