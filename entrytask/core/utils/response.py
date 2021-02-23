from django.forms.models import model_to_dict
from django.http import JsonResponse


def json_response(obj):
    return JsonResponse(model_to_dict(obj))
