from django.urls import path

from catalog.apps import MainConfig
from catalog.views import homepage, contact, product, add_product

app_name = MainConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('contact/', contact, name='contact'),
    path('products/<int:pk>', product, name='product'),
    path('products/add_product', add_product, name='add_product'),
]
