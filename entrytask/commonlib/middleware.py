import json
import time

from django.utils.deprecation import MiddlewareMixin

from commonlib.cache import cache
from commonlib.utils.logger import log
from commonlib.utils.response import json_response


class VerifyTokenMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_view(self, request, *args, **kwargs):
		if request.path[:9] == '/api/user' or request.path[:6] == '/media':
			return None
		header_token = request.META.get('HTTP_AUTHORIZATION', '')
		token = header_token[6:]
		user_data = cache.get(token)
		if user_data is None:
			return json_response(error='Unauthorized')
		if request.path[:6] == '/admin' and user_data['role'] != 2:
			return json_response(error='Permission denied')

		request.user_data = user_data
		return None


class RequestLogMiddleware(MiddlewareMixin):
	def __init__(self, *args, **kwargs):
		super(RequestLogMiddleware, self).__init__(*args, **kwargs)

	def process_request(self, request):
		if request.method in ['POST', 'PUT', 'PATCH']:
			request.req_body = request.body
		if str(request.get_full_path()).startswith('/api/'):
			request.start_time = time.time()

	def extract_log_info(self, request, response=None, exception=None):
		log_data = {
			'remote_address': request.META['REMOTE_ADDR'],
			'request_method': request.method,
			'request_path': request.get_full_path(),
			'run_time': round((time.time() - request.start_time) * 1000, 2),
		}
		if request.method in ['PUT', 'POST', 'PATCH']:
			log_data['request_body'] = json.loads(
				str(request.req_body).encode('utf-8'))
			if response:
				if response['content-type'] == 'application/json':
					response_body = response.content
					log_data['response_body'] = response_body[:200]
		return log_data

	def process_response(self, request, response):
		if str(request.get_full_path()).startswith('/api/'):
			log_data = self.extract_log_info(request=request, response=response)
			log.info(msg=log_data, extra=log_data)
		return response

	def process_exception(self, request, exception):
		log.exception(msg="Unhandled Exception")
		return None
