import json

import bcrypt
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from commonlib.constant import RANDOM_KEY_LENGTH, LOGIN_CACHE_TIMEOUT, SESSION_TIMEOUT, TOKEN_LENGTH
from commonlib.db_crud.role import get_user_role
from commonlib.db_crud.user import insert_user, get_user_by_id, get_user_by_username
from commonlib.schema import user_login_schema, user_register_schema, user_logout_schema
from commonlib.utils.response import error_response, json_response
from commonlib.utils.utils import string_generator, decrypt, hasher, validate_user, validate_token_func


class UserView(View):
	def get(self, *args, **kwargs):
		user_id = int(self.kwargs.get('user_id'))
		user = get_user_by_id(user_id)
		if user is None:
			return json_response(error='User not found')
		return json_response(data={'id': user.id, 'username': user.username, 'fullname': user.fullname})


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
				return json_response(error='Register user unsuccessful')
			return json_response(data={'msg': 'registered'})
		except ValidationError:
			return json_response(error='Wrong data type')


class UserPreloginView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		username = body_json.get('username')

		user = cache.get('{}_userinfo'.format(username))
		if user is None:
			user = model_to_dict(get_user_by_username(username))
			if user is None:
				return json_response(error='Username does not exist')

		random_key = cache.get('{}_key'.format(username))
		if random_key is None:
			random_key = string_generator(RANDOM_KEY_LENGTH)

		cache.set('{}_key'.format(username), random_key, LOGIN_CACHE_TIMEOUT)
		cache.set('{}_userinfo'.format(username), user, SESSION_TIMEOUT)

		return json_response(data={'key': random_key})


class UserLoginView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, user_login_schema)
			username = body_json.get('username')
			encrypted_password = body_json.get('password')
			user_key = cache.get('{}_key'.format(username))

			if user_key is None:
				return json_response(error='Username does not exist or wrong password')

			cache.delete('{}_key'.format(username))
			password = decrypt(encrypted_password, user_key)
			user, is_valid = validate_user(username, password)

			if not is_valid:
				return json_response(error='Username does not exist or wrong password')

			token = string_generator(TOKEN_LENGTH)
			cache.set(token, {'id': user['id'], 'role': get_user_role(user['id']), 'username': user['username']}, SESSION_TIMEOUT)
			return json_response(data={'token': token, 'user_id': user['id']})
		except ValidationError:
			return json_response(error='Input validation error')


class UserLogoutView(View):
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, user_logout_schema)
			if validate_token_func(body_json["token"], body_json["user_id"]):
				cache.delete(body_json["token"])
				return json_response(data={'msg': 'logged out'})
			return json_response(error='Bad request')
		except ValidationError:
			return json_response(error='Bad request')
