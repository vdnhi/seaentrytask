from core.models import Participation


def insert_participation(event_id, user_id):
    participation = Participation.objects.get_or_create(event_id=event_id, user_id=user_id)
    return participation


def get_participation_of_event(event_id):
    list_participant = list(Participation.objects.filter(event_id=event_id))
    return list_participant


def remove_participation(event_id, user_id):
    row_affected = Participation.objects.filter(event_id=event_id, user_id=user_id).delete()
    return row_affected
