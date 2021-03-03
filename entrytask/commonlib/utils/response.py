from django.http import JsonResponse


def json_response(error=None, data=None):
	return JsonResponse({
		'error': error,
		'data': data
	})


def error_response(status_code, error_msg):
	response = JsonResponse({'error': error_msg})
	response.status_code = status_code
	return response
