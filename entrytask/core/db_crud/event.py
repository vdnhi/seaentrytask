from django.forms import model_to_dict

from core.db_crud.channel import get_channel_id_by_name
from core.models import Event, EventChannelMapping


def insert_event(event_data):
	event = Event.objects.create(
		title=event_data.get('title', None),
		content=event_data.get('content', None),
		start_date=int(event_data.get('start_date', None)),
		end_date=int(event_data.get('end_date', None)),
		create_uid=int(event_data.get('create_uid', None)),
		create_time=int(event_data.get('create_time', None)),
		update_time=int(event_data.get('update_time', None)),
		location=event_data.get('location', None),
	)
	return event


def get_events(conditions, base, offset):
	events = list(Event.objects.filter(**conditions).order_by('-create_time', '-id')[base:base + offset])
	events = [model_to_dict(event) for event in events]
	return events


def get_events_with_channels(conditions, channels, base, offset):
	channel_ids = [get_channel_id_by_name(channel) for channel in channels]
	mappings = set(
		EventChannelMapping.objects.filter(channel_id__in=channel_ids).values_list('event_id', flat=True))
	events = Event.objects.filter(**conditions).order_by('-create_time', '-id').values_list('id', flat=True)
	events_in_page = []
	for index in range(len(events)):
		if events[index] not in mappings:
			continue
		if base > 0:
			base -= 1
		else:
			events_in_page.append(events[index])
		if len(events_in_page) == offset:
			break
	events = list(Event.objects.filter(id__in=events_in_page).order_by('-create_time', '-id'))
	events = [model_to_dict(event) for event in events]
	return events


def get_event_by_id(event_id):
	event = Event.objects.filter(id=event_id).first()
	return event


def update_event(event_id, new_data):
	event = get_event_by_id(event_id)
	for key, value in new_data.items():
		if not hasattr(event, key):
			return None
		setattr(event, key, value)
	event.save()
	return event


def delete_event(event_id):
	return Event.objects.filter(id=event_id).delete()
