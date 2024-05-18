from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductDetailView, ContactTemplateView, HomePageView, ProductDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('product/<int:pk>/view', ProductDetailView.as_view(), name='product_view'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
]
