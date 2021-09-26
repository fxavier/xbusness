from django.db import models 
from decimal import Decimal

from .person import Person


class Customer(Person):
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))