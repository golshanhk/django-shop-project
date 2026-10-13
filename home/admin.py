from django.contrib import admin
from .models import *

class Product_variantinlines(admin.TabularInline):
    model = Variant
    extre = 2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'update', 'is_active','sub_category']
    search_fields = ['name']
    list_filter = ['create', 'is_active']
    ordering = ['-create']
    prepopulated_fields={'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'unit_price',
        'discount',
        'total_price',
        'amount',
        'available',
        'create',
    ]
    search_fields = ['name']
    list_filter = ['category', 'available', 'create']
    ordering = ['-create']
    list_editable=['amount']
    raw_id_fields = ['category']
    inlines = [Product_variantinlines]

class CommentAdmin(admin.ModelAdmin):
    list_display=['user','create','rate']

admin.site.register(Variant)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Comment,CommentAdmin)
