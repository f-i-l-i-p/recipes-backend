"""
Helper functions for making requests.
"""


def create_and_log_in_user(client, name=None, email=None, pw=None) -> str:
    user_name, user_email, user_pw = _get_user_info(name, email, pw)

    create_user(client, user_name, user_email, user_pw)
    return log_in_user(client, user_email, user_pw)


def create_user(client, name=None, email=None, pw=None) -> None:
    user_name, user_email, user_pw = _get_user_info(name, email, pw)

    client.post('users/create', json={'user_name': user_name, 'email': user_email, 'password': user_pw})


def log_in_user(client, email, pw) -> str:
    user_name, user_email, user_pw = _get_user_info(None, email, pw)

    res = client.post('auth/login', json={'email': user_email, 'password': user_pw})
    return res.json['token']


def create_recipe(client, token, recipe_name='recipe', recipe_ingredients='an ingredient\n' * 100,
                  recipe_instructions='an instruction\n' * 100, recipe_image='image' * 10000) -> None:
    client.post('recipes/create',
                json={'name': recipe_name, 'ingredients': recipe_ingredients,
                      'instructions': recipe_instructions, 'image': recipe_image},
                headers={'Authorization': f'Bearer {token}'})


def _get_user_info(user_name=None, email=None, user_pw=None):
    if not user_name:
        user_name = "test-user"
    if not email:
        email = user_name + "@example.com"
    if not user_pw:
        user_pw = "password"

    return user_name, email, user_pw
