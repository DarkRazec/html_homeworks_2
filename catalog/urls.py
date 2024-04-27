from django.urls import path

from catalog.views import homepage, contact_info

urlpatterns = [
    path('', homepage),
    path('contact/', contact_info)
]
