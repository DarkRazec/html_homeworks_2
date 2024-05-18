from django.shortcuts import render
from django.views.generic import DetailView

from catalog.models import Product, Contact, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"


def homepage(request):
    category_list = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        price = request.POST.get("price")
        try:
            category = Category.objects.get(id=request.POST.get("category"))
        except ValueError:
            category = None

        Product.objects.create(
            name=name,
            desc=desc,
            image=image,
            category=category,
            price=price,
        )
    context = {
        'product_list': Product.objects.all(),
        'catalog_list': category_list,
        'title': 'Главная',
    }
    return render(request, 'catalog/homepage.html', context)


def contact(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data/contact.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name} {phone} {message}\n")
    context = {
        'object_list': contacts,
        'title': 'Контакты',
    }
    return render(request, 'catalog/contact.html', context)
