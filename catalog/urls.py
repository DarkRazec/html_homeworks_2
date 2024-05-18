from django.urls import path

from catalog.apps import MainConfig
from catalog.views import homepage, contact, ProductDetailView

app_name = MainConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/view', ProductDetailView.as_view(), name='view'),
]
