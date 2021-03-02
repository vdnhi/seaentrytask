import json
import time

from django.core.files.storage import default_storage
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from core.custom_views.schema import event_schema, comment_schema, event_patch_schema, like_schema, participation_schema
from core.db_crud.channel import get_channels, get_event_channels, insert_event_channel
from core.db_crud.comment import get_event_comments, insert_comment
from core.db_crud.event import get_events, get_event_by_id, insert_event, update_event, delete_event, \
	get_events_with_channels
from core.db_crud.image import insert_image, insert_image_to_event, get_event_images
from core.db_crud.like import insert_like, get_like_of_event, remove_like, get_event_like_count, is_user_liked_event
from core.db_crud.participation import get_participation_of_event, insert_participation, remove_participation, \
	get_event_participation_count, is_user_participated_event
from core.db_crud.user import get_user_by_id
from core.utils.decorator import error_handler
from core.utils.http_status_code import HttpStatus
from core.utils.response import json_response, error_response
from core.utils.utils import validate_token_func


class EventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		raw_conditions = {
			'start_date__gte': self.request.GET.get('from'),
			'end_date__lte': self.request.GET.get('to'),
			'location': self.request.GET.get('location')
		}

		base = int(self.request.GET.get('base', 0))
		offset = int(self.request.GET.get('offset', 10))

		filtered_conditions = {k: v for k, v in raw_conditions.items() if v is not None}
		if self.request.GET.get('channels') is not None:
			channels = self.request.GET.get('channels').split(',')
			events = get_events_with_channels(filtered_conditions, channels, base, offset)
		else:
			events = get_events(filtered_conditions, base, offset)

		if events is None or len(events) == 0:
			return json_response([])

		is_logged_user = False
		user_id = self.request.GET.get('user_id', None)
		token = self.request.GET.get('token', None)
		if user_id is not None and token is not None:
			try:
				user_id = int(user_id)
				validate_token_func(token, user_id)
				is_logged_user = True
			except ValidationError:
				pass

		for event in events:
			event['channels'] = get_event_channels(event.get('id'))
			event['image_urls'] = get_event_images(event.get('id'))
			event['count_like'] = get_event_like_count(event.get('id'))
			event['count_participation'] = get_event_participation_count(event.get('id'))
			if is_logged_user:
				event['has_liked'] = is_user_liked_event(user_id, event.get('id'))
				event['has_participated'] = is_user_participated_event(user_id, event.get('id'))

		return json_response(events)

	@error_handler
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, event_schema)
			validate_token_func(body_json["token"], body_json["create_uid"], body_json['role'], require_admin=True)

			current_timestamp = int(time.time())
			body_json["create_time"] = current_timestamp
			body_json["update_time"] = current_timestamp
			event = insert_event(body_json)
			if event is None:
				return error_response(HttpStatus.BadRequest, 'missing data field or wrong data type')

			for channel in body_json["channels"]:
				insert_event_channel(event_id=event.id, channel_id=channel['id'])

			return json_response(event)
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'missing data field or wrong data type (exception)')


class SingleEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		event = get_event_by_id(event_id)
		if event is None:
			return json_response({})

		event = model_to_dict(event)

		event['count_like'] = get_event_like_count(event_id)
		event['count_participation'] = get_event_participation_count(event_id)

		user_id = self.request.GET.get('user_id', None)
		token = self.request.GET.get('token', None)
		if user_id is not None and token is not None:
			try:
				user_id = int(user_id)
				validate_token_func(token, user_id)
				event['has_liked'] = is_user_liked_event(user_id, event.get('id'))
				event['has_participated'] = is_user_participated_event(user_id, event.get('id'))
			except ValidationError:
				pass

		return json_response(event)

	@error_handler
	def patch(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, event_patch_schema)
			validate_token_func(body_json['token'], body_json['create_uid'], role=body_json['role'], require_admin=True)
			event = update_event(event_id, body_json)
			if event is None:
				return error_response(HttpStatus.InternalServerError, 'update failed')
			return json_response(event)
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'invalid input')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		user_id = int(self.request.GET.get('user_id'))
		token = self.request.GET.get('token')
		role = int(self.request.GET.get('role', 0))
		try:
			validate_token_func(token, user_id, role, require_admin=True)
			row_affected = delete_event(event_id)
			if row_affected is None or row_affected[0] == 0:
				return error_response(HttpStatus.InternalServerError, 'delete failed')
			return json_response({'msg': 'deleted event {}'.format(event_id)})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, '')


class ChannelView(View):
	@error_handler
	def get(self, *args, **kwargs):
		base = int(self.request.GET.get('base', 0))
		offset = int(self.request.GET.get('offset', 10))
		channels = get_channels(base, offset)
		return JsonResponse(channels, safe=False)


class UploadImageView(View):
	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		incoming_files = self.request.FILES.getlist('image')
		if len(incoming_files) == 0:
			return error_response(HttpStatus.NotFound, 'no image found')

		for afile in incoming_files:
			filename = default_storage.save(afile.name, afile)
			image_id = insert_image('/media/' + filename)
			insert_image_to_event(event_id, image_id)

		return json_response({'msg': 'upload images successful'})


class LikeEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = int(self.request.GET.get('base', 0))
		offset = int(self.request.GET.get('offset', 10))

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
			validate_token_func(body_json['token'], body_json['user_id'])
			insert_like(event_id, body_json["user_id"])
			return json_response({'msg': 'liked'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, 'invalid input')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		try:
			user_id = int(self.request.GET.get('user_id', 0))
			token = self.request.GET.get('token')
			validate_token_func(token, user_id)

			row_affected = remove_like(event_id, user_id)
			if row_affected == 0:
				return error_response(HttpStatus.NotFound, 'not found')
			return json_response({'msg': 'deleted'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, '')


class ParticipationEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = int(self.request.GET.get('base', 0))
		offset = int(self.request.GET.get('offset', 10))

		list_participant = get_participation_of_event(event_id, base, offset)
		users_id = [participant.user_id for participant in list_participant]
		user_raw_data = [get_user_by_id(user_id) for user_id in users_id]
		user_data = [{'id': user.id, 'username': user.username} for user in user_raw_data]

		return json_response(user_data)

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, participation_schema)
			validate_token_func(body_json['token'], body_json['user_id'])
			insert_participation(event_id, body_json['user_id'])
			return json_response({'msg': 'participated'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, '')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		try:
			user_id = int(self.request.GET.get('user_id', 0))
			token = self.request.GET.get('token')
			validate_token_func(token, user_id)
			row_affected = remove_participation(event_id, user_id)
			if row_affected == 0:
				return error_response(HttpStatus.NotFound, 'not found')
			return json_response({'msg': 'deleted'})
		except ValidationError:
			return error_response(HttpStatus.Unauthorized, '')


class CommentEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = self.request.GET.get('base', 0)
		offset = self.request.GET.get('offset', 10)
		comments = get_event_comments(event_id, base, offset)

		return json_response({'base': base, 'offset': offset, 'comments': comments})

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, comment_schema)
			validate_token_func(body_json['token'], body_json['user_id'])

			timestamp = time.time()
			comment_data = {
				'user_id': body_json['user_id'],
				'event_id': event_id,
				'content': body_json['content'],
				'create_time': timestamp,
				'update_time': timestamp
			}
			insert_comment(comment_data)
			return json_response({'msg': 'ok'})
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'invalid input')
