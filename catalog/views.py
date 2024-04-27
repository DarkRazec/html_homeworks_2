from django.shortcuts import render


def homepage(request):
    return render(request, 'catalog/homepage.html')


def contact_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data/contact.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name} {phone} {message}\n")

    return render(request, 'catalog/contact_info.html')
