from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'added_at']
    list_filter = ['category']
    search_fields = ['name']
    list_per_page = 10