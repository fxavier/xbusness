from django.db import models 

from .person import Person


class Transporter(Person):
    
    class Meta:
        verbose_name = 'Transporter'  
        

class Vehicle(models.Model):
    vehicle_transporter = models.ForeignKey('core.Transporter', related_name='vehicle', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    registration_plate = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self):
        return u'%s / %s ' % (self.description, self.registration_plate)