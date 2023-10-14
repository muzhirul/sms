from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
# Create your models here.
class Grade(models.Model):
    start_mark = models.IntegerField()
    end_mark = models.IntegerField()
    point = models.DecimalField(max_digits=4,decimal_places=2,verbose_name='Grade Point')
    name = models.CharField(max_length=5,verbose_name='Grade Name')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    sl_no = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='grade_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='grade_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_grade'
        constraints = [
            models.CheckConstraint(check=models.Q(point__gte=0), name='grade_point_non_negative'),
            models.CheckConstraint(check=models.Q(point__lte=5), name='grade_point_not_over_five'),
        ]
    
    def __str__(self):
        return self.name