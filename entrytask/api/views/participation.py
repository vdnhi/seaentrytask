import json

from django.views.generic.base import View
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from commonlib.constant import PAGING_SIZE
from commonlib.db_crud.participation import get_participation_of_event, insert_participation, remove_participation
from commonlib.db_crud.user import get_user_by_id
from commonlib.schema import participation_schema
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response


class ParticipationEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = int(self.request.GET.get('base', 0))
		offset = min(int(self.request.GET.get('offset', PAGING_SIZE)), PAGING_SIZE)

		list_participant = get_participation_of_event(event_id, base, offset)
		users_id = [participant.user_id for participant in list_participant]
		user_raw_data = [get_user_by_id(user_id) for user_id in users_id]
		user_data = [{'id': user.id, 'username': user.username} for user in user_raw_data]

		return json_response(data=user_data)

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, participation_schema)
			insert_participation(event_id, body_json['user_id'])
			return json_response(data={'msg': 'participated'})
		except ValidationError:
			return json_response(error='Invalid behavior')

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		user_id = int(self.request.GET.get('user_id', 0))
		row_affected = remove_participation(event_id, user_id)
		if row_affected == 0:
			return json_response(error='Event not found')
		return json_response(data={'msg': 'deleted'})
