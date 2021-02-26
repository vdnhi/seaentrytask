from django.db import DatabaseError
from django.forms import model_to_dict

from core.models import Event
from django.core.exceptions import ObjectDoesNotExist


def insert_event(event_data):
    try:
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
    except (TypeError, DatabaseError):
        return None


def get_events(conditions, base, offset):
    try:
        events = list(Event.objects.filter(**conditions).order_by('-create_time', '-id'))[base:base + offset]
        events = [model_to_dict(event) for event in events]
        return events
    except ObjectDoesNotExist:
        return None


def get_event_by_id(event_id):
    try:
        event = Event.objects.filter(id=event_id).first()
        return event
    except ObjectDoesNotExist:
        return None


def update_event(event_id, new_data):
    try:
        event = get_event_by_id(event_id)
        for key, value in new_data.items():
            if not hasattr(event, key):
                return None
            setattr(event, key, value)
        event.save()
        return event
    except DatabaseError:
        return None


def delete_event(event_id):
    try:
        return Event.objects.filter(id=event_id).delete()
    except DatabaseError:
        return None
