from django.contrib import admin

from goods.models import Category, Product, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'created_at', 'is_published')
#     list_filter = ('created_at', 'is_published')
#     search_fields = ('title', 'body')
