from typing import List
from django.http import HttpResponse
from django.shortcuts import render

from products.models import Product, ProductPrice
from scrapers.scripts.base_spider import Spider

from importlib import import_module

from playwright.sync_api import sync_playwright, Playwright

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("http://example.com")
    # other actions...
    browser.close()


def scrape_products_prices(request):
    product_codes = request.GET.getlist('codes')
    products = Product.objects.filter(code__in=product_codes)

    # browser = await Spider().get_browser()

    with sync_playwright() as playwright:
        run(playwright, products)
    
    return HttpResponse("DONE!")

def run(playwright: Playwright, products):
    
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()

    for _product in products:
        # Get all ProductNameLocations for a better scraping
        product_name_locations = _product.product_name_at_locations.all()

        for product_name_location in product_name_locations:
            script_name = product_name_location.location.script_name
            module = import_module(f"scrapers.scripts.{script_name}")
            price = module.scrape(browser, product_name_location)
            ProductPrice.objects.create(product=product_name_location, price=price)
