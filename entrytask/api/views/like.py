import json

from django.views.generic.base import View
from jsonschema import validate, ValidationError

from commonlib.constant import OFFSET_LIMIT, HttpStatus
from commonlib.db_crud.like import get_like_of_event, insert_like, remove_like
from commonlib.db_crud.user import get_user_by_id
from commonlib.schema import like_schema
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response, error_response


class LikeEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = int(self.request.GET.get('base', 0))
		offset = min(int(self.request.GET.get('offset', 10)), OFFSET_LIMIT)

		likes = get_like_of_event(event_id, base, offset)
		users_id = [like.user_id for like in likes]
		user_raw_data = [get_user_by_id(user_id) for user_id in users_id]
		user_data = [{'id': user.id, 'username': user.username} for user in user_raw_data]

		return json_response(user_data)

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, like_schema)
			insert_like(event_id, body_json["user_id"])
			return json_response({'msg': 'liked'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, 'invalid input')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		try:
			user_id = int(self.request.GET.get('user_id', 0))
			row_affected = remove_like(event_id, user_id)
			if row_affected == 0:
				return error_response(HttpStatus.NotFound, 'not found')
			return json_response({'msg': 'deleted'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, '')
