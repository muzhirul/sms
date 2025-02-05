from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError(
            _('The field cannot contain numbers.'),
            code='no_numbers',
        )

def validate_alpha_chars_only(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('The field can only contain alphabetic characters.'),
            code='alpha_chars_only'
        )

def setup_code():
    last_leave_code = Setup.objects.all().order_by('code').last()
    if not last_leave_code or last_leave_code.code is None:
        return 'S-' + '01'
    leave_num = str(last_leave_code.code)[-2:]
    leave_num_int = int(leave_num)
    new_leave_num = leave_num_int + 1
    new_gd_num = 'S-' + str(new_leave_num).zfill(2)
    return new_gd_num  
# Create your models here.
class Setup(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_setup')
    code = models.CharField(max_length=20, null=True,blank=True, verbose_name='Setup Code',default=setup_code)
    type = models.CharField(max_length=30, blank=True,null=True, verbose_name='Setup Type')
    title = models.CharField(max_length=255, blank=True,null=True, verbose_name='Setup Title')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    sq_order = models.IntegerField(blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='setup_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='setup_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_setup'

    def __str__(self):
        return str(self.type)

class Religion(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Religion Name')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='religion_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='religion_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_religion'

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Gender Name')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='gender_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='gender_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_gender'

    def __str__(self):
        return self.name

class BloodGroup(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Blood Group Name')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='blood_group_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='blood_group_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_b_group'

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Occupation Name')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='occupation_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='occupation_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_occupation'

    def __str__(self):
        return self.name

class Relation(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Relation')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='relation_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='relation_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_relation'

    def __str__(self):
        return self.name

class Menu(models.Model):
    parent = models.ForeignKey( 'self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_menu')
    name = models.CharField(max_length=50, blank=True,null=True, verbose_name='Menu Name')
    slug = models.SlugField(max_length=55, blank=True, null=True)
    icon = models.ImageField(upload_to='menu_icon/',blank=True, null=True, verbose_name='Icon')
    icon_text = models.TextField(blank=True, null=True, verbose_name='Icon Text')
    level = models.IntegerField(blank=True, null=True, verbose_name='Menu Level')
    sl_no = models.IntegerField(blank=True, null=True, verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='menu_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='menu_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_menu'

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='role_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='role_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_role'

    def __str__(self):
        return str(self.name)

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, blank=True, null=True)
    can_create = models.BooleanField(default=False, verbose_name='Create')
    can_view = models.BooleanField(default=True, verbose_name='View')
    can_update = models.BooleanField(default=False, verbose_name='Update')
    can_delete = models.BooleanField(default=False, verbose_name='Delete')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='permission_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='permission_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 's_permission'

    def __str__(self):
        return str(self.id)
    
class Days(models.Model):
    short_name = models.CharField(max_length=5, validators=[validate_alpha_chars_only])
    long_name = models.CharField(max_length=20, validators=[validate_alpha_chars_only])
    sl_no = models.IntegerField()
    week_end = models.BooleanField(default=False) 
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='days_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='days_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_day'

    def __str__(self):
        return self.long_name

class FloorType(models.Model):
    name = models.CharField(max_length=20, verbose_name='Floor Type')
    sl_no = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,
                                related_name='floor_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,
                                related_name='floor_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_floor_type'

    def __str__(self):
        return self.name

class SubjectType(models.Model):
    name = models.CharField(max_length=20, verbose_name='Subject Type')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sub_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='sub_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_subject_type'

    def __str__(self):
        return self.name

class EducationBoard(models.Model):
    board_code = models.CharField(max_length=3, verbose_name='Board Code', validators=[validate_alpha_chars_only])
    name = models.CharField(max_length=50, verbose_name='Board Name', validators=[validate_alpha_chars_only])
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='edu_board_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='edu_board_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_edu_board'

    def __str__(self):
        return self.name

class Country(models.Model):
    coun_code = models.CharField(max_length=4, verbose_name='Country Code', validators=[validate_alpha_chars_only])
    name = models.CharField(max_length=50, verbose_name='Country Name', validators=[validate_alpha_chars_only])
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='country_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='country_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_country'

    def __str__(self):
        return self.name

class Division(models.Model):
    divi_code = models.CharField(max_length=4, verbose_name='Division Code', validators=[validate_alpha_chars_only])
    name = models.CharField(max_length=50, verbose_name='Division Name', validators=[validate_alpha_chars_only])
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='division_creator', editable=False)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='division_update_by', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_division'

    def __str__(self):
        return self.name

class District(models.Model):
    dist_code = models.CharField(max_length=4, verbose_name='District Code', validators=[validate_alpha_chars_only])
    name = models.CharField(max_length=50, verbose_name='District Name', validators=[validate_alpha_chars_only])
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='district_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='district_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_district'

    def __str__(self):
        return self.name

class Thana(models.Model):
    thana_code = models.CharField(max_length=4, verbose_name='Thana Code', validators=[validate_alpha_chars_only])
    name = models.CharField(max_length=50, verbose_name='Thana Name', validators=[validate_alpha_chars_only])
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='thana_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='thana_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_thana'

    def __str__(self):
        return self.name

class ContractType(models.Model):
    name = models.CharField(max_length=100,verbose_name='Contract Type',validators=[validate_alpha_chars_only])
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='con_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='con_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_contract_type'

    def __str__(self):
        return self.name
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=100,verbose_name='Marital Status',validators=[validate_alpha_chars_only])
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='marital_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='marital_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_marital_status'

    def __str__(self):
        return self.name

class AttendanceType(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True)
    ordering = models.IntegerField(blank=True,null=True)
    display = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='attend_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='attend_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_attend_type'

    def __str__(self):
        return str(self.name)
    
class HolidayType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, verbose_name='Color Code')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='holi_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='holi_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 's_holiday_type'

    def __str__(self):
        return str(self.name)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, verbose_name='Payment Method')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='pay_method_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='pay_method_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'set_payment_method'

    def __str__(self):
        return str(self.name)

class ActiveStatus(models.Model):
    name = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='active_status_creator', editable=False)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='active_status_update_by', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'setup_active_status'

    def __str__(self):
        return str(self.name)
    
class SystemCounter(models.Model):
    code = models.CharField(max_length=100, verbose_name='Counter Code')
    name = models.CharField(max_length=100, verbose_name='Counter Name')
    counter_width = models.IntegerField(blank=True, null=True)
    fiscal_year_as_prefix = models.BooleanField(default=False)
    prefix = models.CharField(max_length=20,blank=True,null=True)
    separator = models.CharField(max_length=2,blank=True,null=True)
    step = models.IntegerField(default=1)
    next_number = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sys_counter_creator', editable=False)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='sys_counter_update_by', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'setup_sys_counter'

    def __str__(self):
        return str(self.name)
