from django.db import models
from institution.models import Institution, Branch
from academic.models import *
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_alpha_chars_only(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('The field can only contain alphabetic characters.'),
            code='alpha_chars_only'
        )

# Create your models here.
class FeesType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Fees Type Name',validators=[validate_alpha_chars_only])
    code = models.SlugField(max_length=255)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_type'

    def __str__(self):
        return str(self.name)
    
class FeesDiscount(models.Model):
    name = models.CharField(max_length=255, verbose_name='Fees Name Discount',validators=[validate_alpha_chars_only])
    code = models.SlugField(max_length=255)
    percentage = models.DecimalField(blank=True, null=True,verbose_name='Discount %',max_digits=4,decimal_places=2)
    amount = models.PositiveIntegerField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    remarks= models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_discount_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_discount_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_discount'
        constraints = [
            models.CheckConstraint(check=models.Q(percentage__gte='0'), name='discount_pct_non_negative'),
        ]

    def __str__(self):
        return str(self.name)
    
class FeesMaster(ClassSection):

    class Meta:
        proxy = True
        verbose_name = 'Fees Master'

class FeesDetails(models.Model):
    FINE_TYPE = ((0,'None'),(1,'Percentage'),(2,'Fix Amount'))
    fees_master = models.ForeignKey(FeesMaster, on_delete=models.CASCADE)
    fees_type = models.ForeignKey(FeesType,on_delete=models.CASCADE)
    due_date = models.DateField(blank=True,null=True,verbose_name='Due Date')
    amount = models.DecimalField(blank=True, null=True,verbose_name='Amount',max_digits=10,decimal_places=2)
    fine_type = models.IntegerField(blank=True,null=True,choices=FINE_TYPE)
    percentage = models.DecimalField(blank=True, null=True,verbose_name='Percentage %',max_digits=10,decimal_places=2)
    fix_amt = models.PositiveIntegerField(blank=True,null=True, verbose_name='Fix Amount')
    description = models.TextField(blank=True,null=True)
    remarks= models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_dtl'

    def __str__(self):
        return str(self.fees_type)


