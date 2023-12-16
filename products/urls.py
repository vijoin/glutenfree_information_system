from django.urls import path
from . import views

urlpatterns = [
    path("product-list", views.product_list, name="product_list"),
    path("upload-xlsx", views.upload_products, name="upload-xlsx")
]