from setup_app.models import *
from authentication.models import Authentication
from account.models import AccountLedger
from setup_app.models import SystemCounter

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
    last_voucher_no = AccountLedger.objects.filter(institution=institution, branch=branch).last()
    if voucher_type == 'PAYMENT':
        prefix = 'PV-'
    elif voucher_type == 'RECEIVE':
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
    
def generate_random_payment_id():
    import random, string
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(13))

def generate_code(institution, branch, c_type):
    from datetime import datetime
    if c_type=='PAYMENT' or c_type=='RECEIVE' or c_type=='JOURNAL':
        n_type = 'Voucher'
    else:
        n_type = c_type
    counter = SystemCounter.objects.get(institution=institution, branch=branch, name__iexact=n_type)
    if counter.fiscal_year_as_prefix:
        prefix = str(datetime.now().year)
    else:
        if c_type =='PAYMENT':
            prefix = 'PV'
        elif c_type=='RECEIVE':
            prefix = 'RV'
        else:
            prefix = counter.prefix or ""
    next_number = counter.next_number
    separator = counter.separator or ""

    if counter.counter_width:
        total_code_width = counter.counter_width
        fixed_width = len(prefix) + len(counter.separator or "")
        number_width = total_code_width - fixed_width
        number_str = str(next_number).zfill(number_width)
    else:
        number_str = str(next_number)
    
    final_code = f"{prefix}{separator}{number_str}"

    new_next_number = counter.next_number + counter.step

    counter.next_number = new_next_number
    counter.save()

    return final_code
    