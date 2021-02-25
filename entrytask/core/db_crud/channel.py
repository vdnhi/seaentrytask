from core.models import Channel


def get_all_channels():
    channels = list(Channel.objects.all())
    channels = [{'id': channel.id, 'name': channel.name} for channel in channels]
    return channels


def insert_channel(name):
    channel = Channel.objects.create(name=name)
    return channel
