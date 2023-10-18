from django.db import models
from institution.models import Institution, Branch
from academic.models import ClassName, ClassRoom, Section, Session, Subject, Version
from django_userforeignkey.models.fields import UserForeignKey

from staff.models import Staff
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
        db_table = 'e_grade'
        constraints = [
            models.CheckConstraint(check=models.Q(point__gte=0), name='grade_point_non_negative'),
            models.CheckConstraint(check=models.Q(point__lte=5), name='grade_point_not_over_five'),
        ]
    
    def __str__(self):
        return self.name
    
class ExamName(models.Model):
    name = models.CharField(max_length=50, verbose_name='Exam Name')
    sl_no = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(Session,on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='exam_name_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='exam_name_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'e_exam_name'
    
    def __str__(self):
        return self.name
    
class ExamRoutine(models.Model):
    exam_date = models.DateField()
    day = models.CharField(max_length=20,verbose_name='Exam Day')
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField()
    exam = models.ForeignKey(ExamName, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Staff, verbose_name='Teacher')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='exam_routine_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='exam_routine_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'e_exam_routine'
        
    
    