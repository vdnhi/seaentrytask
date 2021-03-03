import json
import os
import tempfile
import time

from django.core.files.storage import default_storage
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from commonlib.constant import HttpStatus, VALID_IMAGE_EXTENSIONS
from commonlib.db_crud.channel import insert_event_channel
from commonlib.db_crud.event import insert_event, update_event, delete_event
from commonlib.db_crud.image import insert_image, insert_image_to_event
from commonlib.schema import event_schema, event_patch_schema
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response, error_response


class AdminEventView(View):
	@error_handler
	def post(self, *args, **kwargs):
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, event_schema)
			current_timestamp = int(time.time())
			body_json["create_time"] = current_timestamp
			body_json["update_time"] = current_timestamp
			event = insert_event(body_json)
			if event is None:
				return json_response(error='missing data field or wrong data type')

			for channel in body_json["channels"]:
				insert_event_channel(event_id=event.id, channel_id=channel['id'])

			return json_response(data=event)
		except ValidationError:
			return json_response(error='missing data field or wrong data type')


class AdminSingleEventView(View):
	@error_handler
	def patch(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, event_patch_schema)
			event = update_event(event_id, body_json)
			if event is None:
				return error_response(HttpStatus.InternalServerError, 'update failed')
			return json_response(event)
		except ValidationError:
			return error_response(HttpStatus.BadRequest, 'invalid input')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		try:
			row_affected = delete_event(event_id)
			if row_affected is None or row_affected[0] == 0:
				return json_response(error='Event not found')
			return json_response(data={'msg': 'deleted event {}'.format(event_id)})
		except ValidationError:
			return json_response(error='Unauthorized')


class UploadImageView(View):
	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		incoming_files = self.request.FILES.getlist('image')
		if len(incoming_files) == 0:
			return error_response(HttpStatus.NotFound, 'no image found')

		for afile in incoming_files:
			ext = os.path.splitext(afile.name)[1]
			if not ext.lower() in VALID_IMAGE_EXTENSIONS:
				continue
			filename = default_storage.save(tempfile.NamedTemporaryFile(prefix='image') + ext, afile)
			image_id = insert_image('/media/' + filename)
			insert_image_to_event(event_id, image_id)

		return json_response(data={'msg': 'Upload images successful'})
