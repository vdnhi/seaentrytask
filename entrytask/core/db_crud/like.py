from core.models import Like


def insert_like(event_id, user_id):
    like = Like.objects.get_or_create(event_id=event_id, user_id=user_id)
    return like


def get_like_of_event(event_id):
    likes = list(Like.objects.filter(event_id=event_id))
    return likes


def remove_like(event_id, user_id):
    row_affected = Like.objects.filter(event_id=event_id, user_id=user_id).delete()
    return row_affected
