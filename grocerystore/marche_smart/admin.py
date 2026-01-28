from django.contrib import admin
from .models import Product, Category, Owner, Customer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock')
    list_filter = ('category', 'in_stock', 'price')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'in_stock')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
    )


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
