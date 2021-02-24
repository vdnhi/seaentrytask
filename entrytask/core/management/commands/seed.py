import time
import random

from django.core.management import BaseCommand

from core.db_crud.event import insert_event
from core.models import Event

MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('seed done.')


def generate_random_events(limit):
    print('Generating random events...')
    time_delta = 1000
    count_failed = 0
    for index in range(limit):
        event_data = {
            'title': 'Random title {}'.format(index),
            'content': 'Random content {}'.format(index),
            'start_date': int(time.time()),
            'end_date': int(time.time() + time_delta),
            'create_time': int(time.time()),
            'update_time': int(time.time()),
            'create_uid': random.randint(0, limit),
            'location': 'Location {}'.format(index),
            'channel': 'Channel {}'.format(index),
            'image_url': 'image_url'
        }
        event = insert_event(event_data)
        if event is None:
            count_failed += 1

    print('{} events was generated, failed {}'.format(limit - count_failed, count_failed))


def clear_data():
    Event.objects.all().delete()


def run_seed(self, mode):
    clear_data()
    if mode == MODE_CLEAR:
        return

    limit = 100
    generate_random_events(limit)
