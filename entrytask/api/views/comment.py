import json
import time

from django.views.generic.base import View
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from commonlib.constant import PAGING_SIZE
from commonlib.db_crud.comment import get_event_comments, insert_comment
from commonlib.schema import comment_schema
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response


class CommentEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = self.request.GET.get('base', 0)
		offset = min(int(self.request.GET.get('offset', PAGING_SIZE)), PAGING_SIZE)
		comments = get_event_comments(event_id, base, offset)

		return json_response(data={'base': base, 'offset': len(comments), 'comments': comments})

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		body_json = json.loads(self.request.body)
		try:
			validate(body_json, comment_schema)
			timestamp = time.time()
			comment_data = {
				'user_id': body_json['user_id'],
				'event_id': event_id,
				'content': body_json['content'],
				'create_time': timestamp,
				'update_time': timestamp
			}
			insert_comment(comment_data)
			return json_response(data='Comment posted')
		except ValidationError:
			return json_response(error='Invalid input data')
