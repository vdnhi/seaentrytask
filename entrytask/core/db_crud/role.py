from core.models import Role, UserRoleMapping


def get_rolename(role_id):
    role = list(Role.objects.filter(id=role_id))[0]
    return role.rolename


def get_user_role(user_id):
    mapping = UserRoleMapping.objects.filter(user_id=user_id)
    if len(mapping) == 0:
        return ''
    return get_rolename(mapping.model.role_id)
