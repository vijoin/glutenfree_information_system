from django.db import models
from django.db.models import Subquery, OuterRef, Max, Min, DecimalField, IntegerField
from django.db.models.functions import Coalesce



class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    base_url = models.CharField(max_length=200, blank=True)
    get_product_url = models.CharField(max_length=200, blank=True)
    script_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=10)
    generic_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.generic_name} ({self.brand.name})"

    # def get_latest_prices(self):
    #     # Subquery to get the latest timestamp for each location
    #     latest_timestamp_subquery = ProductPrice.objects.filter(
    #         product__product=self
    #     ).order_by('-timestamp').values('timestamp')[:1]

    #     # Query to get the latest price for each location
    #     latest_prices = ProductPrice.objects.filter(
    #         product__product=self,
    #         timestamp=Subquery(latest_timestamp_subquery)
    #     ).annotate(
    #         latest_price=Coalesce('price', 0),
    #         location_name=OuterRef('product__location__name')
    #     ).values('location_name', 'latest_price')

    #     return latest_prices

    # def get_max_latest_price(self):
    #     # Get the maximum value of the latest prices
    #     max_latest_price = self.get_latest_prices().aggregate(Max('latest_price', output_field=DecimalField()))['latest_price__max']
    #     return max_latest_price

    # def get_min_latest_price(self):
    #     # Get the minimum value of the latest prices
    #     min_latest_price = self.get_latest_prices().aggregate(Min('latest_price', output_field=DecimalField()))['latest_price__min']
    #     return min_latest_price

    def get_latest_prices(self):
        # Use aggregation to get the latest price for each location
        latest_prices = ProductPrice.objects.filter(
            product__product=self
        ).values('product__location__name').annotate(
            latest_price=Coalesce(Max('price', output_field=IntegerField()), 0)
        ).values('product__location__name', 'latest_price')

        return latest_prices

    def get_max_latest_price(self):
        # Get the maximum value of the latest prices
        max_latest_price = ProductPrice.objects.filter(
            product__product=self
        ).aggregate(max_latest_price=Coalesce(Max('price', output_field=IntegerField()), 0))['max_latest_price']

        return max_latest_price

    def get_min_latest_price(self):
        # Get the minimum value of the latest prices
        min_latest_price = ProductPrice.objects.filter(
            product__product=self
        ).aggregate(min_latest_price=Coalesce(Min('price', output_field=IntegerField()), 0))['min_latest_price']

        return min_latest_price
    
class ProductNameLocation(models.Model):
    """Save different names at different stores for the same product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_name_at_locations")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="product_names")
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.product.brand}) at {self.location}"

class ProductPrice(models.Model):
    product = models.ForeignKey(ProductNameLocation, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField(auto_now_add=True)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="product_prices_at_locations")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}: {self.price} at {self.product.location.name}"

    class Meta:
        ordering = ("-timestamp",)
