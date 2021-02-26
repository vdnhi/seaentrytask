import time
import random

import bcrypt
from django.core.management import BaseCommand

from core.db_crud.channel import insert_channel
from core.db_crud.comment import insert_comment
from core.db_crud.event import insert_event
from core.db_crud.image import insert_image, insert_image_to_event
from core.db_crud.role import insert_role, insert_user_role
from core.db_crud.user import insert_user
from core.models import Event, Role, User, UserRoleMapping
from core.utils.utils import hasher


class Command(BaseCommand):
    help = "seed database for testing and development"

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed(self)
        self.stdout.write('Seed done.')


def generate_events(limit):
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


def generate_users(limit):
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


def generate_channels(limit):
    print('Generating channel...')
    count_failed = 0
    for i in range(limit):
        channel = insert_channel('Channel {}'.format(i))
        if channel is None:
            count_failed += 1
    print('Channel generation done with failed = {}'.format(count_failed))


def generate_images(limit):
    print('Generating images...')
    count_failed = 0
    for i in range(limit):
        image_id = insert_image("/media/foody_vVhdaLV.jpeg")
        mapping = insert_image_to_event(i, image_id)
        if mapping is None:
            count_failed += 1
    print('Images generation done with failed = {}'.format(count_failed))


def generate_comments(limit):
    print('Generating comments...')
    count_failed = 0
    for i in range(limit):
        timestamp = time.time()
        comment_data = {
            'user_id': i,
            'event_id': i,
            'content': 'Content {}'.format(i),
            'create_time': timestamp,
            'update_time': timestamp
        }
        comment_id = insert_comment(comment_data)
        if comment_id is None:
            count_failed += 1
    print('Comments generation done with failed = {}'.format(count_failed))


def run_seed(self):
    limit = 1000000
    generate_events(limit)
    generate_roles()
    generate_users(limit)
    generate_user_role_mapping(limit)
    generate_channels(limit)
    generate_images(limit)
    generate_comments(limit)
