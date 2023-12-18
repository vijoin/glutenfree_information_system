from django.urls import path
from . import views

urlpatterns = [
    path("scrape-product-prices", views.scrape_products_prices, name="scrape_products_prices"),
]