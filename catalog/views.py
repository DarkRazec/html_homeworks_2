from django.shortcuts import render

from catalog.models import Product, Contact


def homepage(request):
    products = (Product.objects.all()).reverse()
    return render(request, 'catalog/homepage.html', locals())


def contact_info(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('country')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data/contact.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name} {phone} {message}\n")

    return render(request, 'catalog/contact_info.html', locals())
