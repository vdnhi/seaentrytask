from django.db import DatabaseError

from core.models import Role, UserRoleMapping


def insert_role(rolename):
    try:
        role = Role.objects.create(rolename=rolename)
        return role
    except DatabaseError:
        return None


def insert_user_role(user_id, role_id):
    try:
        role = UserRoleMapping.objects.create(user_id=user_id, role_id=role_id)
        return role
    except DatabaseError:
        return None


def get_rolename(role_id):
    role = list(Role.objects.filter(id=role_id))[0]
    return role.rolename


def get_user_role(user_id):
    mapping = UserRoleMapping.objects.filter(user_id=user_id)
    if len(mapping) == 0:
        return ''
    return get_rolename(mapping.model.role_id)
