from core.models import User


def insert_user(user_info):
    user = User.objects.create(
        username=user_info.get('username', None),
        salted_password=user_info.get('username', None),
        email=user_info.get('email', None),
    )
    return user


def get_user(user_id):
    user = list(User.objects.filter(id=user_id))[0]
    return user
