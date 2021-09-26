from django.db import models 

from .person import Person

class Provider(Person):
    branch = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.branch
