user_login_schema = {
	'type': 'object',
	'required': ['username', 'password', 'role'],
	'properties': {
		'username': {'type': 'string'},
		'password': {'type': 'string'},
		'role': {'type': 'number'}
	}
}

user_logout_schema = {
	'type': 'object',
	'required': ['user_id', 'token'],
	'properties': {
		'user_id': 'number',
		'token': 'string'
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

get_event_schema = {
	'type': 'object',
	'properties': {
		'from': {'type': 'number'},
		'to': {'type': 'number'},
		'channels': {'type': 'string'},
		'location': {'type': 'string'},
		'base': {'type': 'number'},
		'offset': {'type': 'number'},
	}
}

event_schema = {
	'type': 'object',
	'required': ['title', 'content', 'location', 'start_date', 'end_date', 'create_uid', 'token', 'role'],
	'properties': {
		'title': {'type': 'string'},
		'content': {'type': 'string'},
		'location': {'type': 'string'},
		'start_date': {'type': 'number'},
		'end_date': {'type': 'number'},
		'channels': {
			'type': 'array',
			'items': {
				'type': 'object',
				'properties': {
					'id': {'type': 'number'},
					'name': {'type': 'string'}
				}
			}
		},
		'create_uid': {'type': 'number'},
		'token': {'type': 'string'},
		'role': {'type': 'number'}
	}
}

event_patch_schema = {
	'type': 'object',
	'required': ['create_uid', 'token', 'role'],
	'properties': {
		'title': {'type': 'string'},
		'content': {'type': 'string'},
		'location': {'type': 'string'},
		'start_date': {'type': 'number'},
		'end_date': {'type': 'number'},
		'channels': {
			'type': 'array',
			'items': {
				'type': 'object',
				'properties': {
					'id': {'type': 'number'},
					'name': {'type': 'string'}
				}
			}
		},
		'create_uid': {'type': 'number'},
		'token': {'type': 'string'},
		'role': {'type': 'number'}
	}
}

like_schema = {
	'type': 'object',
	'required': ['user_id', 'token'],
	'properties': {
		'user_id': {'type': 'number'},
		'token': {'type': 'string'},
	}
}

comment_schema = {
	'type': 'object',
	'required': ['user_id', 'content', 'token'],
	'properties': {
		'user_id': {'type': 'number'},
		'content': {'type': 'string'},
		'token': {'type': 'string'},
	}
}

participation_schema = {
	'type': 'object',
	'required': ['user_id', 'token'],
	'properties': {
		'user_id': {'type': 'number'},
		'token': {'type': 'string'},
	},
}
