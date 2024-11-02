from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import UniqueConstraint
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.
class Warehouse(models.Model):
    CATEGORY = [
        ('FINISHED_GOODS','Finished Goods'),
        ('RAW_MATERIALS',"Raw Materials"),
    ]

    name = models.CharField(max_length=255,verbose_name='Warehouse Name')
    keyword = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=255, verbose_name='Warehouse Category', choices=CATEGORY)
    as_default = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='warehouse_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='warehouse_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_warehouse'
        verbose_name = 'Warehouse'
        constraints = [
            UniqueConstraint(fields=['name','is_active','status','institution','branch'], name='warehouse_unique_constraint')
        ] 
    def __str__(self):
        return str(self.name)
    
@receiver(post_save, sender=Warehouse)
def set_as_default(sender, instance, **kwargs):
    if instance.as_default:
        sender.objects.filter(institution=instance.institution, branch=instance.branch,status=True,category=instance.category).exclude(id=instance.id).update(as_default=False)

class Brand(models.Model):
    name = models.CharField(max_length=255,verbose_name='Brand Name')
    keyword = models.CharField(max_length=255,verbose_name='Keyword', blank=True, null=True,editable=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='brand_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='brand_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_brand'
        verbose_name = 'Brand'
        constraints = [
            UniqueConstraint(fields=['name','keyword','status','institution','branch'], name='brand_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.name:
            self.keyword = self.name.upper().replace(' ','_').replace('-', '_')
        super(Brand,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
