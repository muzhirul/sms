from django.db import models
from institution.models import Institution, Branch
from academic.models import ClassName, ClassRoom, Section, Session, Subject, Version
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
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
    day = models.CharField(max_length=20,verbose_name='Exam Day',blank=True,null=True, editable=False)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DurationField(blank=True,null=True)
    exam = models.ForeignKey(ExamName, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Staff, verbose_name='Teacher')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='exam_routine_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='exam_routine_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # @property
    # def duration(self):
    #     if self.start_time and self.end_time:
    #         return self.end_time - self.start_time
    #     return None
        
    class Meta:
        db_table = 'e_exam_routine'
        
@receiver(pre_save, sender=ExamRoutine)        
def calculate_duration(sender, instance, **kwargs):
    if instance.start_time and instance.end_time:
        # Get the current date for the calculation
        current_date = datetime.now().date()

        # Convert start_time and end_time to datetime objects
        start_datetime = datetime.combine(current_date, instance.start_time)
        end_datetime = datetime.combine(current_date, instance.end_time)

        # Ensure both start_time and end_time are on the same date
        if start_datetime > end_datetime:
            # In case end_time is on the next day, adjust it
            end_datetime += timedelta(days=1)

        duration = end_datetime - start_datetime
        instance.duration = duration
    else:
        instance.duration = None
        
@receiver(pre_save, sender=ExamRoutine)          
def find_day(sender, instance, **kwargs):
    
    if instance.exam_date:
        date_string = str(instance.exam_date)
        date = datetime.strptime(date_string, "%Y-%m-%d")
        # Get the day name
        day_name = date.strftime("%A")
        instance.day = day_name
    else:
        instance.day = None

    
    