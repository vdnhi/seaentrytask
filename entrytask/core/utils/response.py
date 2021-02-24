from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse


def json_response(data):
    if isinstance(data, dict):
        return JsonResponse(data)
    return JsonResponse(model_to_dict(data))


def error_response(status_code, error_msg):
    response = JsonResponse({'error': error_msg})
    response.status_code = status_code
    return response


def json_list_response(data):
    return HttpResponse(serialize('json', data), content_type='application/json')
