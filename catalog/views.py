from django.shortcuts import render

from catalog.models import Product, Contact, Category


def homepage(request):
    category_list = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        try:
            category = Category.objects.get(id=request.POST.get("category"))
        except ValueError:
            category = None
        price = request.POST.get("price")

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


def product(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {
        'object': prod,
        'title': prod.name,
    }
    return render(request, 'catalog/product.html', context)


def add_product(request):
    category_list = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        category = Category.objects.get(id=request.POST.get("category"))
        price = request.POST.get("price")

        Product.objects.create(
            name=name,
            desc=desc,
            image=image,
            category=category,
            price=price,
        )

    context = {
        'object_list': category_list,
        'title': 'Добавить продукт'
    }
    return render(request, 'catalog/add_product.html', context)


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
