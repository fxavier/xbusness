from django.db import models 
from decimal import Decimal
from django.core.validators import MinValueValidator

from core.utils import product_image_file_path, category_image_file_path, unique_slug_generator
from django.db.models.signals import pre_save, post_save


PRODUCT_STATE = (
    ('Novo', 'Novo'),
    ('Usado', 'Usado')
)

TAG = (
    ('Oferta do dia', 'Oferta do dia'),
    ('Quente', 'Quente'),
    ('Mais vendido', 'Mais Vendido')
)

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
    

class Coupon(models.Model):
    name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    
    def __str__(self):
        return self.name
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
    sale_price_old = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.CASCADE)
    sale_price_new = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    state = models.CharField(max_length=10, choices=PRODUCT_STATE, null=True, blank=True)
    tag = models.CharField(max_length=100, choices=TAG, null=True, blank=True)
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
    
    
# class ProductImage(models.Model):
#     image = models.ImageField(upload_to=product_image_file_path)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Product Images'
    
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(category_pre_save_receiver, sender=Category)

   
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(product_pre_save_receiver, sender=Product)

def price_new_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.sale_price_new:
        instance.sale_price_new = instance.sale_price_old * (1 - instance.coupon.discount / 100)

pre_save.connect(price_new_pre_save_receiver, sender=Product)