from django.db import models
from institution.models import Institution, Branch
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
