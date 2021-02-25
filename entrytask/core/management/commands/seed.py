import time
import random

import bcrypt
from django.core.management import BaseCommand

from core.db_crud.channel import insert_channel
from core.db_crud.event import insert_event
from core.db_crud.role import insert_role, insert_user_role
from core.db_crud.user import insert_user
from core.models import Event, Role, User, UserRoleMapping
from core.utils.utils import hasher

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
        }
        event = insert_event(event_data)
        if event is None:
            count_failed += 1

    print('{} events were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_roles():
    insert_role('user')
    insert_role('admin')


def generate_random_users(limit):
    print('Generating random users...')
    count_failed = 0
    for i in range(limit):
        salt = bcrypt.gensalt()
        user_data = {
            'username': 'user{}'.format(i),
            'fullname': 'User {}'.format(i),
            'email': 'user{}@foody.vn'.format(i),
            'salt': salt,
            'salted_password': hasher('user{}'.format(i), salt)
        }
        user = insert_user(user_data)
        if user is None:
            count_failed += 1
    print('{} users were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_user_role_mapping(limit):
    print('Generating user role mapping...')
    count_failed = 0
    for i in range(limit):
        mapping = insert_user_role(i + 1, 1 + (i % 2))
        if mapping is None:
            count_failed += 1
    print('{} user role mapping were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_channels():
    print('Generating channel...')
    for i in range(10):
        insert_channel('Channel {}'.format(i))
    print('Channel generation done!')


def clear_data():
    Event.objects.all().delete()
    Role.objects.all().delete()
    User.objects.all().delete()
    UserRoleMapping.objects.all().delete()


def run_seed(self, mode):
    clear_data()
    if mode == MODE_CLEAR:
        return

    limit = 100
    generate_random_events(limit)
    generate_roles()
    generate_random_users(limit)
    generate_user_role_mapping(limit)
    generate_channels()
