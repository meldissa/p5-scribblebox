from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'name',
        'comment',
        'created_on',
        'approved',
    )
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
