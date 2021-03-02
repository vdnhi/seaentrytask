import random
import time

import bcrypt
from django.core.management import BaseCommand

from commonlib.db_crud import insert_role, insert_user_role
from commonlib.db_crud.user import insert_user
from commonlib.models import Event, User, UserRoleMapping, Channel, Image, Comment, Role, EventChannelMapping, Like, \
    Participation, EventImageMapping
from commonlib.utils.utils import hasher

NUM_ADMIN = 10
BATCH_SIZE = 10000


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
	batch = []
	for index in range(limit):
		batch.append(Event(
			title='Random title {}'.format(index),
			content='Random content{}'.format(index),
			start_date=int(time.time()),
			end_date=int(time.time() + time_delta),
			create_time=int(time.time()),
			update_time=int(time.time()),
			create_uid=random.randint(limit, limit + NUM_ADMIN),
			location='Location {}'.format(index)
		))

		if len(batch) == BATCH_SIZE:
			events = Event.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(events)
			batch = []

	print('{} events were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_roles(limit):
	print('Generating roles...')
	insert_role('user')
	insert_role('admin')
	batch = []
	count_failed = 0
	for index in range(limit):
		batch.append(Role(rolename='Role {}'.format(index)))
		if len(batch) == BATCH_SIZE:
			roles = Role.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(roles)
			batch = []

	print('Generated roles with failed = {}'.format(count_failed))


def generate_users(limit):
	print('Generating random users...')
	count_failed = 0
	batch = []

	for i in range(limit):
		salt = bcrypt.gensalt()
		batch.append(User(
			username='user{}'.format(i),
			fullname='Fullname {}'.format(i),
			email='emailuser{}@foody.vn'.format(i),
			salt=salt,
			salted_password=hasher('user{}'.format(i), salt)
		))

		if len(batch) == BATCH_SIZE:
			users = User.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(users)
			batch = []

	for i in range(NUM_ADMIN):
		salt = bcrypt.gensalt()
		insert_user({
			'username': 'admin{}'.format(i),
			'fullname': 'Admin {}'.format(i),
			'email': 'admin{}@foody.vn'.format(i),
			'salt': salt,
			'salted_password': hasher('admin{}'.format(i), salt)
		})

	print('{} users were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_user_role_mapping(limit):
	print('Generating user role mapping...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(UserRoleMapping(
			user_id=i + 1,
			role_id=1
		))
		if len(batch) == BATCH_SIZE:
			mappings = UserRoleMapping.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(mappings)
			batch = []

	for i in range(NUM_ADMIN):
		insert_user_role(user_id=limit + i, role_id=2)

	print('{} user role mapping were generated, failed {}'.format(limit - count_failed, count_failed))


def generate_channels(limit):
	print('Generating channel...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(Channel(name='Channel {}'.format(i)))
		if len(batch) == BATCH_SIZE:
			channels = Channel.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			batch = []
			count_failed += BATCH_SIZE - len(channels)

	print('Channel generation done with failed = {}'.format(count_failed))


def generate_event_channel(limit):
	print('Generating event channel...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(EventChannelMapping(
			event_id=random.randint(0, limit),
			channel_id=random.randint(0, limit)
		))

		if len(batch) == BATCH_SIZE:
			mappings = EventChannelMapping.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			batch = []
			count_failed += BATCH_SIZE - len(mappings)

	print('Event channel generated with failed = {}'.format(count_failed))


def generate_likes(limit):
	print('Generating likes...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(Like(
			event_id=random.randint(0, limit),
			user_id=random.randint(0, limit + NUM_ADMIN)
		))

		if len(batch) == BATCH_SIZE:
			likes = Like.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			batch = []
			count_failed += BATCH_SIZE - len(likes)

	print('Generated likes with failed = {}'.format(count_failed))


def generate_participation(limit):
	print('Generating participation...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(Participation(
			user_id=random.randint(0, limit),
			event_id=random.randint(0, limit),
			create_time=time.time()
		))

		if len(batch) == BATCH_SIZE:
			participations = Participation.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			batch = []
			count_failed += BATCH_SIZE - len(participations)

	print('Generated participation with failed = {}'.format(count_failed))


def generate_images(limit):
	print('Generating images...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(Image(image_url='/media/foody.jpeg'))
		if len(batch) == BATCH_SIZE:
			images = Image.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(images)
			batch = []

	print('Images generation done with failed = {}'.format(count_failed))


def generate_event_image(limit):
	print('Generating event images...')
	count_failed = 0
	batch = []
	for i in range(limit):
		batch.append(EventImageMapping(
			image_id=random.randint(0, limit),
			event_id=random.randint(0, limit)
		))

		if len(batch) == BATCH_SIZE:
			mappings = EventImageMapping.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			count_failed += BATCH_SIZE - len(mappings)
			batch = []

	print('Event images generated with failed = {}'.format(count_failed))


def generate_comments(limit):
	print('Generating comments...')
	count_failed = 0
	batch = []
	for i in range(limit):
		timestamp = time.time()
		batch.append(Comment(
			user_id=i,
			event_id=i,
			content='Content {}'.format(i),
			create_time=timestamp,
			update_time=timestamp
		))

		if len(batch) == BATCH_SIZE:
			comments = Comment.objects.bulk_create(batch, batch_size=BATCH_SIZE)
			batch = []
			count_failed += BATCH_SIZE - len(comments)

	print('Comments generation done with failed = {}'.format(count_failed))


def run_seed(self):
	limit = 1000000
	generate_events(limit)
	generate_roles(limit)
	generate_users(limit)
	generate_user_role_mapping(limit)
	generate_channels(limit)
	generate_images(limit)
	generate_comments(limit)
	generate_event_channel(limit)
	generate_likes(limit)
	generate_participation(limit)
	generate_event_image(limit)
