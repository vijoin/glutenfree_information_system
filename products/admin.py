from django.contrib import admin
from .models import Product, ProductCategory, ProductBrand


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "category"]

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
