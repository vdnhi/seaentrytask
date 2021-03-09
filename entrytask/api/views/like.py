from django.views.generic.base import View

from commonlib.constant import PAGING_SIZE
from commonlib.db_crud.like import get_like_of_event, insert_like, remove_like
from commonlib.db_crud.user import get_user_by_ids
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response


class LikeEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		base = int(self.request.GET.get('base', 0))
		offset = min(int(self.request.GET.get('offset', PAGING_SIZE)), PAGING_SIZE)

		likes = get_like_of_event(event_id, base, offset)
		users_id = [like.user_id for like in likes]
		user_data = get_user_by_ids(users_id)

		return json_response(data=user_data)

	@error_handler
	def post(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		user_data = self.request.user_data
		insert_like(event_id, user_data['id'])
		return json_response(data={'msg': 'liked'})

	@error_handler
	def delete(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		user_data = self.request.user_data
		row_affected = remove_like(event_id, user_data['id'])
		if row_affected == 0:
			return json_response(error='User Id or Event id not found')
		return json_response(data={'msg': 'deleted'})
