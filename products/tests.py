from django.test import TestCase
from .models import Product, ProductBrand, ProductCategory, ProductPrice, ProductNameLocation, Location


class ProductTest(TestCase):
    def setUp(self):
        brand = ProductBrand.objects.create(name="Brand1", description="Brand1")
        category = ProductCategory.objects.create(name="Category1", description="Category1")
        product = Product.objects.create(code="A01", generic_name="Product1", brand=brand, category=category)
        location_disco = Location.objects.create(name="Disco")
        location_tata = Location.objects.create(name="Ta-Ta")

        self.product_name_at_disco = ProductNameLocation.objects.create(product=product, location=location_disco, name="Product #1")
        self.product_name_at_tata = ProductNameLocation.objects.create(product=product, location=location_tata, name="Product Number1")

    # def test_product_is_created(self):
    #     product = Product.objects.get(generic_name="Product1")
    #     self.assertEqual(product.generic_name, "Product1")
    #     self.assertEqual(product.brand.name, "Brand1")
    #     self.assertEqual(product.category.name, "Category1")
    
    def test_latest_max_and_min_price(self):
        product = Product.objects.get(generic_name="Product1")

        price1 = ProductPrice.objects.create(product=self.product_name_at_disco, price=99)
        price2 = ProductPrice.objects.create(product=self.product_name_at_tata, price=100)
        # self.product_name_at_disco.prices.add(price1)

        price4 = ProductPrice.objects.create(product=self.product_name_at_tata, price=98)
        price3 = ProductPrice.objects.create(product=self.product_name_at_disco, price=99)
        # product.prices.add(price3, price4)

        self.assertEqual(product.get_min_latest_price(), 98)
        self.assertEqual(product.get_max_latest_price(), 99)

        # price5 = ProductPrice.objects.create(product=self.product_name_at_disco, price=96)
        # price6 = ProductPrice.objects.create(product=self.product_name_at_tata, price=97)
        # product.product_name_at_locations.prices.add(price5, price6)

        # self.assertEqual(product.latest_min_price, 96)
        # self.assertEqual(product.get_min_latest_price(), 96)
        # self.assertEqual(product.get_max_latest_price(), 97)

    # def test_upload_xlsx(self):
    #     # Create a XLSX file
    #     # Send a POST Request imitating the form
    #     # Validate that all products were created, counting them
    #     raise NotImplementedError
