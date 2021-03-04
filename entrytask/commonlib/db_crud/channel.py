from commonlib.models import Channel, EventChannelMapping


def insert_channel(name):
	channel = Channel.objects.create(name=name)
	return channel


def insert_event_channel(event_id, channel_id):
	created = EventChannelMapping.objects.create(event_id=event_id, channel_id=channel_id)
	return created


def get_channels(base, offset):
	channels = list(Channel.objects.all().order_by('id')[base:base + offset])
	channels = [{'id': channel.id, 'name': channel.name} for channel in channels]
	return channels


def get_channel_id_by_name(channel_name):
	channel = list(Channel.objects.filter(name__icontains=channel_name))
	if len(channel) == 0:
		return None
	return channel[0].id


def get_channel_name_by_id(channel_id):
	channel = list(Channel.objects.filter(id=channel_id))
	if len(channel) == 0:
		return None
	return channel[0].name


def get_channel_name_by_ids(channel_ids):
	return list(Channel.objects.filter(id__in=channel_ids).values_list('id', 'name'))


def get_event_channels(event_id):
	channel_ids = EventChannelMapping.objects.filter(event_id=event_id).values_list('channel_id', flat=True)
	channel_names = [{'id': channel[0], 'name': channel[1]} for channel in get_channel_name_by_ids(channel_ids)]
	return channel_names
