from django.forms import model_to_dict
from django.http import JsonResponse


def json_response(error=None, data=None):
	if data is not None and not isinstance(data, dict) and not isinstance(data, list):
		data = model_to_dict(data)
	return JsonResponse({
		'error': error,
		'data': data
	})


def error_response(status_code, error_msg):
	response = JsonResponse({'error': error_msg})
	response.status_code = status_code
	return response
