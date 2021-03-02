import json

from django.core.cache import cache
from jsonschema import ValidationError

from commonlib.constant import HttpStatus
from commonlib.utils.response import error_response


def validate_token(function):
	def _inner_function(self, *args, **kwargs):
		if self.request.method == 'POST':
			body_json = json.loads(self.request.body)
			token = body_json.get('token')
			user_id = body_json.get('user_id')
			role = body_json.get('role')
		else:
			token = self.request.GET.get('token')
			user_id = self.request.GET.get('user_id')
			role = int(self.request.GET.get('role', 0))

		if cache.get(token) is None:
			raise ValidationError('')

		cached_data = cache.get(token)

		if user_id != cached_data['id']:
			raise ValidationError('')

		if role != cached_data['role']:
			raise ValidationError('')

		function(self)

	return _inner_function


def error_handler(func):
	def _inner_function(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as exception:
			print(exception.message)
			return error_response(HttpStatus.InternalServerError, exception.message)

	return _inner_function
