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
	lst = list(Channel.objects.filter(id__in=channel_ids).values_list('id', 'name'))
	mapping = {}
	for channel in lst:
		mapping[channel[0]] = channel[1]
	return mapping


def get_events_channels(event_ids):
	list_mapping = EventChannelMapping.objects.filter(event_id__in=event_ids).values_list('channel_id', 'event_id')
	list_channel_id = []
	channel_id_existed = {}
	result = {}
	for item in list_mapping:
		channel_id = item[0]
		event_id = item[1]

		if channel_id not in channel_id_existed:
			list_channel_id.append(channel_id)
			channel_id_existed[channel_id] = True
		if event_id not in result:
			result[event_id] = [channel_id]
		else:
			result[event_id].append(channel_id)

	channel_names = get_channel_name_by_ids(list_channel_id)
	for _, item in result.items():
		for i in range(len(item)):
			item[i] = {'id': item[i], 'name': channel_names[item[i]]}

	return result
