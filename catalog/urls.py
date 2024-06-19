from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import MainConfig
from catalog.views import ProductDetailView, ContactTemplateView, HomePageView, ProductDeleteView, ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_view'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
]
