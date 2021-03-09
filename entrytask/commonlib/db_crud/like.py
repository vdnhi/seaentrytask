from django.core.cache import cache
from django.db.models import Count

from commonlib.models import Like


def insert_like(event_id, user_id):
	like = Like.objects.get_or_create(event_id=event_id, user_id=user_id)
	return like


def get_event_like_count(event_id):
	count = cache.get('event_like_count_' + str(event_id))
	if count is not None:
		return count
	count = Like.objects.filter(event_id=event_id).count()
	cache.st('event_like_count_' + str(event_id), count)
	return count


def get_events_like_count(event_ids):
	uncached = []
	like_count = {}
	for event_id in event_ids:
		count = cache.get('event_like_count_' + str(event_id))
		if count is not None:
			like_count[event_id] = count
		else:
			uncached.append(event_id)

	like_list = list(Like.objects.filter(event_id__in=uncached).values('event_id').annotate(count=Count('event_id')))
	for data in like_list:
		like_count[data['event_id']] = data['count']
		cache.set('event_like_count_' + str(data['event_id']), data['count'])
	return like_count


def get_like_of_event(event_id, base, offset):
	likes = list(Like.objects.filter(event_id=event_id)[base:base + offset])
	return likes


def remove_like(event_id, user_id):
	row_affected = Like.objects.filter(event_id=event_id, user_id=user_id).delete()
	return row_affected


def get_events_user_liked(user_id):
	return set(Like.objects.filter(user_id=user_id).values_list('event_id', flat=True))


def is_user_liked_event(user_id, event_id):
	return Like.objects.filter(event_id=event_id, user_id=user_id).count() > 0
