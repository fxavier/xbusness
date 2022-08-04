from django.db import models 
from decimal import Decimal
from django.core.validators import MinValueValidator

from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save, post_save


from core.utils import product_image_file_path, category_image_file_path, unique_slug_generator



PRODUCT_STATE = (
    ('Novo', 'Novo'),
    ('Usado', 'Usado')
)

TAG = (
    ('Oferta do dia', 'Oferta do dia'),
    ('Quente', 'Quente'),
    ('Mais vendido', 'Mais Vendido'), 
    ('Destacados', 'Destacados')
)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(tag='Destacados', active=True)
    
    def quente(self):
        return self.filter(tag='Quente', active=True)
    
    def maisVendido(self):
        return self.filter(tag='Mais vendido', active=True)
    
    def ofertaDoDia(self):
        return self.filter(tag='Oferta do dia', active=True)

    def search(self, query):
        lookups = (
                  Q(name__icontains=query) | 
                  Q(product_state__icontains=query) |
                  Q(sales_price__icontains=query) |
                  Q(product_state__icontains=query)
                  )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()
    
     
    def quente(self):
        return self.get_queryset().quente()
    
    def maisVendido(self):
        return self.get_queryset().maisVendido()
    
    def ofertaDoDia(self):
        return self.get_queryset().ofertaDoDia()


    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Category(models.Model):
    slug = models.SlugField(null=True, blank=True)
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

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
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
class Product(models.Model):
    code = models.CharField(max_length=30)
    barcode = models.CharField(max_length=16, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.PROTECT)
    unity = models.ForeignKey(Unity, null=True, blank=True, on_delete=models.PROTECT)
    product_state = models.CharField(max_length=255, choices=PRODUCT_STATE, null=True, blank=True)
    cost = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    sales_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    # coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, null=True, blank=True)
    # sale_price_new = models.DecimalField(max_digits=16, decimal_places=2, validators=[
                            #    MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'), null=True, blank=True)
    tag = models.CharField(max_length=100, choices=TAG, null=True, blank=True)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    minimum_stock = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=False)
    
    
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
        return self.name
    
class ImageUpload(models.Model):
    image = models.ImageField(upload_to=product_image_file_path)

    def __str__(self):
        return str(self.image)
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)
    image = models.ForeignKey(ImageUpload, related_name="image_product", on_delete=models.CASCADE)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"{self.product.name} - {self.image}"

    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name="product_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField()
    rate = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)


class Wish(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_wish", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="products_wished")
    created_at = models.DateTimeField(auto_now_add=True)
   
    
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(category_pre_save_receiver, sender=Category)

   
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(product_pre_save_receiver, sender=Product)

# def price_new_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.sale_price_new and instance.coupon:
#         instance.sale_price_new = instance.sale_price_old * (1 - int(instance.coupon.discount) / 100)
#     else:
#         instance.sale_price_new = instance.sale_price_old

# pre_save.connect(price_new_pre_save_receiver, sender=Product)