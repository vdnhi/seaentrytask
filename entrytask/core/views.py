# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.models import model_to_dict
from django.http import JsonResponse

from core.db_crud.role import get_user_role
from db_crud.user import get_user


def test(request):
    user = get_user(1)
    user_dict = model_to_dict(user)
    user_dict['role'] = get_user_role(user.id)
    return JsonResponse(user_dict)