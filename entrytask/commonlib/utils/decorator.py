from commonlib.utils.logger import log
from commonlib.utils.response import json_response


def error_handler(func):
	def _inner_function(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as exception:
			log.error(exception.message)
			return json_response(error=exception.message)

	return _inner_function
