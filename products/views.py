# views.py
import pandas as pd  # Make sure you have pandas installed: pip install pandas
from django.shortcuts import render
from .models import Product, ProductCategory, ProductBrand  # Import your Product model
from django.http import HttpResponseRedirect
from django.urls import reverse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def upload_products(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # Check if the file is an Excel file
        if not file.name.endswith('.xlsx'):
            return render(request, 'upload_form.html', {'error': 'Please upload a valid Excel file'})

        # Use pandas to read the Excel file
        df = pd.read_excel(file)

        # Iterate through the rows and save to the Product model
        for index, row in df.iterrows():
            category_name = row['Categoría']
            name = row['Nombre']
            brand_name = row['Marca']

            # Create or get the Category object
            category, created = ProductCategory.objects.get_or_create(
                name=category_name,
                description=category_name
            )

            # Create or get the Brand object
            brand, created = ProductBrand.objects.get_or_create(
                name=brand_name,
                description=brand_name
            )

            # Create or get the Product object
            product, created = Product.objects.get_or_create(
                category=category,
                brand=brand,
                name=name,
                description=name
            )

            if created:
                print(f"New product created {product.name}")

        # Redirect to a success page or the product list page
        return HttpResponseRedirect(reverse('product_list'))  # Adjust the URL name as needed

    return render(request, 'upload_form.html')