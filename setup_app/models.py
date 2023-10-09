from importlib.abc import Traversable
from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class Setup(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_setup')
    code = models.CharField(max_length=20,null=True,blank=True,verbose_name='Setup Code')
    type = models.CharField(max_length=20,blank=True,null=True,verbose_name='Setup Type')
    title = models.CharField(max_length=50,blank=True,null=True,verbose_name='Setup Title')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    sq_order = models.IntegerField(blank=True,null=True)
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='setup_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='setup_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_setup'
        
    def __str__(self):
        return f"self.type"
    
class Religion(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Religion Name')
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='religion_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='religion_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_religion'
    
    def __str__(self):
        return self.name
    
class Gender(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Gender Name')
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='gender_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='gender_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_gender'
    
    def __str__(self):
        return self.name
    
class BloodGroup(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Blood Group Name')
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='blood_group_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='blood_group_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_b_group'
    
    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Occupation Name')
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='occupation_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='occupation_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_occupation'
    
    def __str__(self):
        return self.name
    
class Relation(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Relation')
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='relation_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='relation_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_relation'
    
    def __str__(self):
        return self.name

class Menu(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_menu')
    name = models.CharField(max_length=50,blank=True,null=True,verbose_name='Menu Name')
    slug = models.SlugField(max_length=55, blank=True, null=True)
    icon = models.ImageField(upload_to='menu_icon/',blank=True, null=True, verbose_name='Icon')
    level = models.IntegerField(blank=True,null=True,verbose_name='Menu Level')
    # create_permission = models.BooleanField(default=False)
    # view_permission = models.BooleanField(default=False)
    # edit_permission = models.BooleanField(default=False)
    # delete_permission = models.BooleanField(default=False)
    sl_no = models.IntegerField(blank=True,null=True,verbose_name='Ordering')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='menu_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='menu_update_by', editable=False, blank=True, null=True)
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
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='role_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 's_role'
        
    def __str__(self):
        return self.name
    
class Permission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,blank=True,null=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL,blank=True,null=True)
    can_create = models.BooleanField(default=False, verbose_name='Create')
    can_view = models.BooleanField(default=True, verbose_name='View')
    can_update = models.BooleanField(default=False, verbose_name='Update')
    can_delete = models.BooleanField(default=False, verbose_name='Delete')
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = 's_permission'
        
    def __str__(self):
        return self.menu.name