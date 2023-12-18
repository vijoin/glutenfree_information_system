from django.contrib import admin
from .models import Product, ProductCategory, ProductBrand, ProductNameLocation, ProductPrice, Location


class ProductAdmin(admin.ModelAdmin):
    list_display = ["generic_name", "brand", "category"]

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

class ProductNameLocationAdmin(admin.ModelAdmin):
    list_display = ["product", "location", "name"]

class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ["product", "timestamp", "price"]

class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "base_url", "get_product_url"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductNameLocation, ProductNameLocationAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(Location, LocationAdmin)

