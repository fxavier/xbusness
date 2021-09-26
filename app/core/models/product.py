from django.db import models 
from decimal import Decimal
from django.core.validators import MinValueValidator


class Category(models.Model):
    slug = models.SlugField()
    description = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __unicode__(self):
        return self.description

class Brand(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description
    
class Unity(models.Model):
    symbol = models.CharField(max_length=3)
    description = models.CharField(max_length=16)
    
    class Meta:
        verbose_name_plural = "Unities"
    
    def __str__(self):
        return self.description
    
    
class Product(models.Model):
    code = models.CharField(max_length=30)
    barcode = models.CharField(max_length=16, null=True, blank=True)
    slug = models.SlugField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.PROTECT)
    unity = models.ForeignKey(Unity, null=True, blank=True, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    sale = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    minimum_stock = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    
    
    @property
    def format_unity(self):
        if self.unity:
            return self.unity.symbol
        else:
            return ''
        
    def get_unity_symbol(self):
        if self.unity:
            return self.unity.symbol
        else: 
            return ''
        
    def __str__(self):
        return self.description
    