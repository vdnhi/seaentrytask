import time

from django.core.cache import cache
from django.db.models import Count

from commonlib.models import Participation


def insert_participation(event_id, user_id):
	timestamp = time.time()
	participation = Participation.objects.get_or_create(event_id=event_id, user_id=user_id, create_time=timestamp)
	return participation


def get_participation_of_event(event_id, base, offset):
	list_participant = list(Participation.objects.filter(event_id=event_id)[base:base + offset])
	return list_participant


def get_event_participation_count(event_id):
	count = cache.get('event_participation_count_' + str(event_id))
	if count is not None:
		return count
	count = Participation.objects.filter(event_id=event_id).count()
	cache.set('event_participation_count_' + str(event_id), count)
	return count


def get_events_participation_count(event_ids):
	uncached = []
	participation_count = {}
	for event_id in event_ids:
		event_participation_count = cache.get('event_participation_count_' + str(event_id))
		if event_participation_count is not None:
			participation_count[event_id] = event_participation_count
		else:
			uncached.append(event_id)

	data_list = list(
		Participation.objects.filter(event_id__in=uncached).values('event_id').annotate(count=Count('event_id')))
	for data in data_list:
		participation_count[data['event_id']] = data['count']
		cache.set('event_participation_count_' + str(data['event_id']), data['count'])
	return participation_count


def remove_participation(event_id, user_id):
	row_affected = Participation.objects.filter(event_id=event_id, user_id=user_id).delete()
	return row_affected


def get_events_user_participated(user_id):
	return set(Participation.objects.filter(user_id=user_id).values_list('event_id', flat=True))


def is_user_participated_event(user_id, event_id):
	return Participation.objects.filter(user_id=user_id, event_id=event_id).count() > 0
