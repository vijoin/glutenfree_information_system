from django.db import models
from django.db.models import Subquery, OuterRef, Max, Min, DecimalField
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


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name
    
    @property
    def latest_max_price(self):
        latest_prices = self.get_latest_prices()

        # Get the maximum value of the latest prices
        max_latest_price = latest_prices.aggregate(Max('latest_price', output_field=DecimalField()))['latest_price__max']

        return max_latest_price

    @property
    def latest_min_price(self):
        latest_prices = self.get_latest_prices()

        # Get the maximum value of the latest prices
        min_latest_price = latest_prices.aggregate(Min('latest_price', output_field=DecimalField()))['latest_price__min']

        return min_latest_price
    
    def get_latest_prices(self):
        """Get most recent prices for each location"""

        # Query to get distinct locations from ProductPrice model
        distinct_locations = ProductPrice.objects.values('location').distinct()

        # Subquery to get the latest timestamp for each location
        latest_timestamp_subquery = ProductPrice.objects.filter(
            location=OuterRef('location')
        ).order_by('-timestamp').values('timestamp')[:1]

        # Query to get the latest price for each location
        latest_prices = ProductPrice.objects.filter(
            location__in=Subquery(distinct_locations.values('location')),
            timestamp=Subquery(latest_timestamp_subquery)
        ).annotate(
            latest_price=Coalesce('price', 0)
        ).values('location', 'latest_price')

        return latest_prices
    

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ("-timestamp",)
