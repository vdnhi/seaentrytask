import json

import bcrypt
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from core.custom_views.schema import user_login_schema, user_register_schema, user_logout_schema
from core.db_crud.user import insert_user, get_user_by_id, get_user_by_username
from core.utils.http_status_code import HttpStatus
from core.utils.response import error_response, json_response
from core.utils.utils import string_generator, decrypt, hasher, validate_user, validate_token_func

LOGIN_CACHE_TIMEOUT = 60
SESSION_TIMEOUT = 3600
TOKEN_LENGTH = 64
RANDOM_KEY_LENGTH = 32


class UserView(View):
	def get(self, *args, **kwargs):
		user_id = int(self.kwargs.get('user_id'))
		user = get_user_by_id(user_id)
		if user is None:
			return error_response(404, 'User not found')
		return json_response({'id': user.id, 'username': user.username, 'fullname': user.fullname})


class UserRegisterView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, user_register_schema)
			password = body_json.get('password')
			salt = bcrypt.gensalt()
			user = insert_user({
				'username': body_json.get('username'),
				'email': body_json.get('email', None),
				'fullname': body_json.get('fullname', None),
				'salt': salt,
				'salted_password': hasher(password, salt)
			})
			if user is None:
				return error_response(500, '')
			return json_response({'msg': 'registered'})
		except ValidationError:
			return error_response(400, 'Invalid field(s) input')


class UserPreloginView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		username = body_json.get('username')
		if cache.get('{}_userinfo'.format(username)) is None:
			user = model_to_dict(get_user_by_username(username))
		else:
			user = cache.get('{}_userinfo'.format(username))

		if user is None:
			error_response(HttpStatus.BadRequest, 'Username does not exist or wrong password')

		if cache.get('{}_key'.format(username)) is None:
			random_key = string_generator(RANDOM_KEY_LENGTH)
		else:
			random_key = cache.get('{}_key'.format(username))

		cache.set('{}_key'.format(username), random_key, LOGIN_CACHE_TIMEOUT)
		cache.set('{}_userinfo'.format(username), user, LOGIN_CACHE_TIMEOUT)
		return json_response({'key': random_key})


class UserLoginView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, user_login_schema)

			username = body_json.get('username')
			encrypted_password = body_json.get('password')
			role = int(body_json.get('role'))

			if cache.get('{}_key'.format(username)) is None:
				return error_response(HttpStatus.BadRequest, 'Username does not exist or wrong password')

			user_key = cache.get('{}_key'.format(username))
			cache.delete('{}_key'.format(username))

			password = decrypt(encrypted_password, user_key)
			user, role, is_valid = validate_user(username, password, role)

			if not is_valid:
				return error_response(HttpStatus.BadRequest, 'Username does not exist or wrong password')

			token = string_generator(TOKEN_LENGTH)
			cache.set(token, {"id": user['id'], "role": role, "username": user['username']}, SESSION_TIMEOUT)
			return json_response({'token': token, 'user_id': user['id'], 'role': role})
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'Username does not exist or wrong password')


class UserLogoutView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, user_logout_schema)
			if validate_token_func(body_json["token"], body_json["user_id"]):
				cache.delete(body_json["token"])
				return json_response({'msg': 'logged out'})
			return error_response(HttpStatus.BadRequest, '')
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'invalid input')
