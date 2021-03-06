from commonlib.models import User


def insert_user(user_info):
	user = User.objects.create(
		username=user_info.get('username'),
		salted_password=user_info.get('salted_password'),
		email=user_info.get('email'),
		salt=user_info.get('salt'),
		fullname=user_info.get('fullname')
	)
	return user


def get_user_by_id(user_id):
	user = User.objects.filter(id=user_id).first()
	return user


def get_user_by_ids(user_ids):
	users = User.objects.filter(id__in=user_ids).values_list('id', 'username')
	return users


def get_user_by_username(username):
	user = User.objects.filter(username=username).first()
	return user


def is_exist_username(username):
	return User.objects.filter(username=username).count() > 0
