from django.core.cache import cache

from commonlib.utils.response import json_response


class VerifyTokenMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_view(self, request, *args, **kwargs):
		if request.path[:9] == '/api/user':
			return None
		header_token = request.META.get('HTTP_AUTHORIZATION', '')
		token = header_token[6:]
		cached_data = cache.get(token)
		if cached_data is None:
			return json_response(error='Unauthorized')
		if request.path[:6] == '/admin' and cached_data['role'] != 2:
			return json_response(error='Permission denied')

		return None

