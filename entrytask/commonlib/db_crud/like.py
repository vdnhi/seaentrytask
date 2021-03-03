from commonlib.models import Like


def insert_like(event_id, user_id):
	like = Like.objects.get_or_create(event_id=event_id, user_id=user_id)
	return like


def get_event_like_count(event_id):
	return Like.objects.filter(event_id=event_id).count()


def get_events_like_count(event_ids):
	like_list = list(Like.objects.filter(event_id__in=event_ids).values_list('event_id', 'user_id'))
	like_count = {}
	for like in like_list:
		if like[0] not in like_count:
			like_count[like[0]] = 1
		else:
			like_count[like[0]] += 1
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
