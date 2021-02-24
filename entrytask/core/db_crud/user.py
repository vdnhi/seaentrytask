from core.models import User


def insert_user(user_info):
    user = User.objects.create(
        username=user_info.get('username', None),
        salted_password=user_info.get('username', None),
        email=user_info.get('email', None),
    )
    return user


def get_user(user_id):
    user = User.objects.filter(user_id=user_id).first()
    return user
