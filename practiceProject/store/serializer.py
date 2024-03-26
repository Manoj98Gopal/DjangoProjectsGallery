from rest_framework import serializers
from .models import Product
from decimal import Decimal



class ProductSerializer(serializers.Serializer):
    
    
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField()
    # here changing the field name 
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    
    
    
    def calculate_tax(self,product:Product):
        
        tax_price = Decimal(1.4)
        return product.unit_price * tax_price
    
    
    
    
    
