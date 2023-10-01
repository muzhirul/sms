from setup_app.models import *
from authentication.models import Authentication

def check_permission(user, menu_name, permission_type='view'):
    user = Authentication.objects.get(id=user)
    role_id = []
    for role in user.role.filter(status=True):
        role_id.append((role.id))
    menu_ids = []
    for menus in Menu.objects.filter(name=menu_name,status=True):
        menu_ids.append((menus.id))
    if permission_type == 'view':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_view=True)
    elif permission_type == 'create':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_create=True)
    elif permission_type == 'update':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_update=True)
    elif permission_type == 'delete':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_delete=True)
    if menu_permissions:
        return True
    return False