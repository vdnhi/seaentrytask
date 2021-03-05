from django.forms import model_to_dict
from django.views.generic.base import View

from commonlib.cache import cache
from commonlib.constant import PAGING_SIZE
from commonlib.db_crud.channel import get_events_channels
from commonlib.db_crud.event import get_events_with_channels, get_events, get_event_by_id
from commonlib.db_crud.image import get_events_images
from commonlib.db_crud.like import get_event_like_count, is_user_liked_event, get_events_like_count, \
	get_events_user_liked
from commonlib.db_crud.participation import get_event_participation_count, is_user_participated_event, \
	get_events_participation_count, get_events_user_participated
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response


class ApiEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		raw_conditions = {
			'start_date__gte': self.request.GET.get('from'),
			'end_date__lte': self.request.GET.get('to'),
			'location': self.request.GET.get('location')
		}

		base = int(self.request.GET.get('base', 0))
		offset = min(int(self.request.GET.get('offset', PAGING_SIZE)), PAGING_SIZE)

		filtered_conditions = {k: v for k, v in raw_conditions.items() if v is not None}
		if self.request.GET.get('channels') is not None:
			channels = self.request.GET.get('channels').split(',')
			events = get_events_with_channels(filtered_conditions, channels, base, offset)
		else:
			events = get_events(filtered_conditions, base, offset)

		if events is None or len(events) == 0:
			return json_response(data=[])

		token = self.request.META.get('HTTP_AUTHORIZATION')[6:]
		user_data = cache.get(token)

		event_ids = [event['id'] for event in events]

		count_like_map = get_events_like_count(event_ids)
		count_participation_map = get_events_participation_count(event_ids)
		events_user_liked = get_events_user_liked(user_data['id'])
		events_user_participated = get_events_user_participated(user_data['id'])
		events_channels = get_events_channels(event_ids)
		event_images = get_events_images(event_ids)

		for event in events:
			event['channels'] = events_channels.get(event.get('id'), None)
			event['image_urls'] = event_images.get(event.get('id'), None)
			event['count_like'] = count_like_map[event.get('id')] if event.get('id') in count_like_map else 0
			event['count_participation'] = count_participation_map[event.get('id')] if event.get(
				'id') in count_participation_map else 0
			event['has_liked'] = event['id'] in events_user_liked
			event['has_participated'] = event['id'] in events_user_participated
		return json_response(data=events)


class ApiSingleEventView(View):
	@error_handler
	def get(self, *args, **kwargs):
		event_id = int(self.kwargs.get('event_id'))
		event = get_event_by_id(event_id)
		if event is None:
			return json_response(data={})

		event = model_to_dict(event)

		event['count_like'] = get_event_like_count(event_id)
		event['count_participation'] = get_event_participation_count(event_id)

		token = self.request.META.get('HTTP_AUTHORIZATION')[6:]
		user_data = cache.get(token)
		event['has_liked'] = is_user_liked_event(user_data['id'], event.get('id'))
		event['has_participated'] = is_user_participated_event(user_data['id'], event.get('id'))

		return json_response(data=event)
