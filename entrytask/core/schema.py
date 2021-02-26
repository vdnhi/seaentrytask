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

event_schema = {
    'type': 'object',
    'required': ['title', 'content', 'location', 'start_date', 'end_date'],
    'properties': {
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'location': {'type': 'string'},
        'start_date': {'type': 'number'},
        'end_date': {'type': 'number'},
        'channels': {'type': 'array'},
        'create_uid': {'type': 'number'}
    }
}

comment_schema = {
    'type': 'object',
    'required': ['user_id', 'content', 'token'],
    'properties': {
        'user_id': {'type': 'number'},
        'content': {'type': 'string'},
        'token': {'type': 'string'}
    }
}
