from django.forms import model_to_dict
from django.http import JsonResponse


def json_response(data):
	if isinstance(data, dict):
		return JsonResponse(data)
	if isinstance(data, list):
		return JsonResponse(data, safe=False)
	return JsonResponse(model_to_dict(data))


def error_response(status_code, error_msg):
	response = JsonResponse({'error': error_msg})
	response.status_code = status_code
	return response

