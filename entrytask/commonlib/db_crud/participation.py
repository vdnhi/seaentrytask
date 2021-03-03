import time

from commonlib.models import Participation


def insert_participation(event_id, user_id):
	timestamp = time.time()
	participation = Participation.objects.get_or_create(event_id=event_id, user_id=user_id, create_time=timestamp)
	return participation


def get_participation_of_event(event_id, base, offset):
	list_participant = list(Participation.objects.filter(event_id=event_id)[base:base + offset])
	return list_participant


def get_event_participation_count(event_id):
	return Participation.objects.filter(event_id=event_id).count()


def get_events_participation_count(event_ids):
	participation_list = list(Participation.objects.filter(event_id__in=event_ids).values_list('event_id', 'user_id'))
	participation_count = {}
	for participation in participation_list:
		if participation[0] not in participation_count:
			participation_count[participation[0]] = 1
		else:
			participation_count[participation[0]] += 1
	return participation_count


def remove_participation(event_id, user_id):
	row_affected = Participation.objects.filter(event_id=event_id, user_id=user_id).delete()
	return row_affected


def get_events_user_participated(user_id):
	return set(Participation.objects.filter(user_id=user_id).values_list('event_id', flat=True))


def is_user_participated_event(user_id, event_id):
	return Participation.objects.filter(user_id=user_id, event_id=event_id).count() > 0
