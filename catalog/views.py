from django.shortcuts import render

from catalog.models import Product, Contact


def homepage(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Главная',
    }
    return render(request, 'catalog/homepage.html', context)


def product(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {
        'object': prod,
        'title': prod.name,
    }
    return render(request, 'catalog/product.html', context)


def contact(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('country')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data/contact.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name} {phone} {message}\n")
    context = {
        'object_list': contacts,
        'title': 'Контакты',
    }
    return render(request, 'catalog/contact.html', context)
