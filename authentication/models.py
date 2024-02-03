from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from institution.models import Institution, Branch
from setup_app.models import Role



class MyAccountManager(BaseUserManager):
    def create_user(self,username,password=None):
        
        if not username:
            raise ValueError('User must have an username.')
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
# Create your models here.
class Authentication(AbstractBaseUser,PermissionsMixin):
    USER_TYPE = (('ADMIN', 'Admin'),('TEACHER', 'Teacher'),('STUDENT', 'Student'), ('GUARDIAN', 'Guardian'), ('ACCOUNTANT', 'Accountant'))
    id = models.UUIDField(primary_key=True, max_length=40, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True,db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=30, blank=True, null=True, choices=USER_TYPE)
    role = models.ManyToManyField(Role,related_name='user_role')
    model_name = models.CharField(max_length=100,blank=True,null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    class Meta:
        db_table = 'authentication'
    
    def __str__(self):
        return self.username
    