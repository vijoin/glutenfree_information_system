from django.urls import path
from . import views
from .views import ProductListView, ProductDetailsView

# urlpatterns = [
#     path("product-list", views.product_list, name="product_list"),
#     path("upload-xlsx", views.upload_products, name="upload-xlsx")
# ]

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path("upload-xlsx", views.upload_products, name="upload-xlsx"),
]