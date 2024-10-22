from setup_app.models import *
from authentication.models import Authentication
from account.models import AccountLedger

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

def generate_voucher_no(institution, branch, voucher_type):
    from datetime import datetime
    if voucher_type == 'PAYMENT':
        last_voucher_no = AccountLedger.objects.filter(institution=institution, branch=branch,voucher_type='PAYMENT').last()
        prefix = 'PV-'
    elif voucher_type == 'RECEIVE':
        last_voucher_no = AccountLedger.objects.filter(institution=institution, branch=branch, voucher_type='RECEIVE').last()
        prefix = 'RV-'
    if not last_voucher_no or last_voucher_no.voucher_no is None:
        voucher_no = prefix +str(datetime.now().date().year)+'1'
    else:
        new_voucher_no = int(last_voucher_no.voucher_no[7:])+1
        voucher_no = prefix + str(datetime.now().date().year) + str(new_voucher_no)
    if voucher_no:
        return voucher_no
    else:
        return None
    