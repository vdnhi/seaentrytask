from core.models import Participation


def insert_participation(event_id, user_id):
    participation = Participation.objects.get_or_create(event_id=event_id, user_id=user_id)
    return participation


def get_participation_of_event(event_id, base, offset):
    list_participant = list(Participation.objects.filter(event_id=event_id)[base:base + offset])
    return list_participant


def get_event_participation_count(event_id):
    return Participation.objects.filter(event_id=event_id).count()


def remove_participation(event_id, user_id):
    row_affected = Participation.objects.filter(event_id=event_id, user_id=user_id).delete()
    return row_affected


def is_user_participated_event(user_id, event_id):
    return Participation.objects.filter(user_id=user_id, event_id=event_id).count() > 0
