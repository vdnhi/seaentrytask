from core.models import Event


def insert_event(event_data):
    event = Event.objects.create(
        title=event_data.get('title', None),
        content=event_data.get('content', None),
        start_date=event_data.get('start_date', None),
        end_date=event_data.get('end_date', None),
        create_uid=event_data.get('create_uid', None),
        create_time=event_data.get('create_time', None),
        update_time=event_data.get('update_time', None),
        location=event_data.get('location', None),
        channel=event_data.get('channel', None),
        image_url=event_data.get('image_url', None)
    )
    return event


def get_event_by_channel(channel):
    events = Event.objects.filter(channel=channel)
    return events


def get_event_by_time_range(start_time, end_time):
    events = Event.objects.filter(start_date__gte=start_time, end_date__lte=end_time)
    return events


def get_event_by_index_range(base, offset):
    events = Event.objects.all()[base:base+offset]
    return events
