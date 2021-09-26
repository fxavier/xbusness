from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=255)
    additional_info = models.CharField(max_length=1025, null=True, blank=True)
    address = models.ForeignKey('core.Address', related_name='address', on_delete=models.CASCADE, blank=True, null=True)
    phone = models.ForeignKey('core.Phone', related_name='phone', on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    bank = models.ForeignKey('core.Bank', related_name='bank', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Update creation date
        if not self.created_at: 
            self.created_at = timezone.now()  
        self.modified_at = timezone.now()
        return super(Person, self).save(*args, **kwargs)
   
class Address(models.Model):
    country = models.CharField(max_length=255, null=True, blank=True, default='Moçambique')
    city = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    
    
    class Meta: 
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self): 
        return self.number
    
    
class Phone(models.Model):
    number = models.CharField(max_length=32)
    
    def __str__(self):
        return self.person_phone
    
class Bank(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    account = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self):
        return self.name