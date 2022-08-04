from rest_framework import serializers

from core.models import product

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = product.Category
        fields = ('id', 'slug', 'name')
        read_onnly_fields = ('id', 'slug',)
        
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=product.Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=product.Brand.objects.all())
    
    class Meta:
        model = product.Product
        # fields = ('category',
        #           'id', 
        #           'code',
        #           'barcode',
        #           'slug',
        #           'name',
        #           'brand',
        #           'unity',
        #           'product_state',
        #           'cost',
        #           'sale_price_old',
        #           'coupon',
        #           'sale_price_new',
        #           'tag',
        #           'additional_info',
        #           'minimum_stock',
        #           'current_stock',
        #           'active'
        #           )
        fields = '__all__'
        read_only_fields = ('id', 'slug',)
        