from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer() # (join db)
    class Meta:
        model = Product
        fields = '__all__'