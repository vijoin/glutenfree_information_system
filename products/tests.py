from django.test import TestCase
from .models import Product, ProductBrand, ProductCategory


class ProductTest(TestCase):
    def setUp(self):
        brand = ProductBrand.objects.create(name="Brand1", description="Brand1")
        category = ProductCategory.objects.create(name="Category1", description="Category1")
        Product.objects.create(name="Product1", brand=brand, category=category)

    def test_product_is_created(self):
        product = Product.objects.get(name="Product1")
        self.assertEqual(product.name, "Product1")
        self.assertEqual(product.brand.name, "Brand1")
        self.assertEqual(product.category.name, "Category1")