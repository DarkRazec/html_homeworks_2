from django.contrib import admin

from catalog.models import Category, Product, Contact, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'phone', 'address')
    list_filter = ('country', 'phone', 'address')
    search_fields = ('country', 'phone', 'address')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'num', 'is_active',)
    list_filter = ('is_active',)
