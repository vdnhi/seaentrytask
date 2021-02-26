import json

import bcrypt
from django.core.cache import cache
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from core.db_crud.user import get_user_salt, insert_user, get_user_by_id
from core.schema import user_login_schema, user_register_schema, user_logout_schema
from core.utils.response import error_response, json_response
from core.utils.utils import string_generator, decrypt, hasher, validate_user, validate_token


class UserView(View):
    def get(self, *args, **kwargs):
        user_id = int(self.kwargs.get('user_id'))
        user = get_user_by_id(user_id)
        if user is None:
            error_response(404, 'User not found')
        return json_response(user)


class UserRegisterView(View):
    def post(self, *args, **kwargs):
        body_json = json.loads(self.request.body)
        try:
            validate(body_json, user_register_schema)
            password = body_json.get('password')
            salt = bcrypt.gensalt()
            user = insert_user({
                'username': body_json.get('username'),
                'email': body_json.get('email', None),
                'fullname': body_json.get('fullname', None),
                'salt': salt,
                'salted_password': hasher(password, salt)
            })
            if user is None:
                return error_response(500, '')
            return json_response({'msg': 'registered'})
        except ValidationError:
            return error_response(400, 'Invalid field(s) input')


class UserPreloginView(View):
    def post(self, *args, **kwargs):
        body_json = json.loads(self.request.body)
        username = body_json.get('username')
        user_salt = get_user_salt(username)
        if user_salt is None:
            error_response(400, 'Username does not exist or wrong password')
        random_key = string_generator(32)
        cache.set('{}_key'.format(username), random_key, 60)
        return json_response({'key': random_key})


class UserLoginView(View):
    def post(self, *args, **kwargs):
        body_json = json.loads(self.request.body)
        try:
            validate(body_json, user_login_schema)

            username = body_json.get('username')
            encrypted_password = body_json.get('password')
            role = int(body_json.get('role'))

            if cache.get('{}_key'.format(username)) is None:
                return error_response(400, 'Username does not exist or wrong password')

            user_key = cache.get('{}_key'.format(username))
            cache.delete('{}_key'.format(username))

            password = decrypt(encrypted_password, user_key)
            user, role, is_valid = validate_user(username, password, role)

            if not is_valid:
                return error_response(400, 'Username does not exist or wrong password')

            token = string_generator(64)
            cache.set(token, {"id": user.id, "role": role, "username": user.username}, 3600)
            return json_response({'token': token, 'user_id': user.id})
        except ValidationError:
            return error_response(400, 'Username does not exist or wrong password')


class UserLogoutView(View):
    def post(self, *args, **kwargs):
        body_json = json.loads(self.request.body)
        try:
            validate(body_json, user_logout_schema)
            if validate_token(body_json["token"], body_json["user_id"]):
                cache.delete(body_json["token"])
                return json_response({'msg': 'logged out'})
            return error_response(400, '')
        except ValidationError:
            return error_response(400, 'invalid input')
