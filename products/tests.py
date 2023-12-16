from django.test import TestCase
from .models import Product, ProductBrand, ProductCategory, ProductPrice


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
    
    def test_latest_max_and_min_price(self):
        product = Product.objects.get(name="Product1")

        price1 = ProductPrice.objects.create(product=product, location="Disco", price=99)
        price2 = ProductPrice.objects.create(product=product, location="Ta-Ta", price=100)
        product.prices.add(price1, price2)

        price3 = ProductPrice.objects.create(product=product, location="Disco", price=99)
        price4 = ProductPrice.objects.create(product=product, location="Ta-Ta", price=98)
        product.prices.add(price3, price4)

        price5 = ProductPrice.objects.create(product=product, location="Disco", price=96)
        price6 = ProductPrice.objects.create(product=product, location="Ta-Ta", price=97)
        product.prices.add(price5, price6)

        self.assertEqual(product.latest_min_price, 96)
        self.assertEqual(product.latest_max_price, 97)
    
    def test_upload_xlsx(self):
        # Create a XLSX file
        # Send a POST Request imitating the form
        # Validate that all products were created, counting them
        raise NotImplementedError