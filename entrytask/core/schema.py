user_login_schema = {
    'type': 'object',
    'required': ['username', 'password', 'role'],
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'number'}
    }
}

user_register_schema = {
    'type': 'object',
    'required': ['username', 'password'],
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string'},
        'fullname': {'type': 'string'}
    }
}
