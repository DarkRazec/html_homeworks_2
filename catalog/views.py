from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView

from catalog.models import Product, Contact, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"


class HomePageView(CreateView):
    model = Product
    fields = ('name', 'desc', 'image', 'price', 'category')
    template_name = 'catalog/homepage.html'
    extra_context = {
        'category_list': Category.objects.all(),
        'title': 'Главная',
    }
    success_url = reverse_lazy('catalog:homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        return context


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contact.html'
    extra_context = {
        'object_list': Contact.objects.all(),
        'title': 'Контакты',
    }

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data/contact.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name} {phone} {message}\n")
        return self.render_to_response(super().get_context_data())


# class HomepageTemplateView(TemplateView):
#     template_name = 'catalog/homepage.html'
#     extra_context = {
#         'category_list': Category.objects.all(),
#         'title': 'Главная',
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product_list'] = Product.objects.all()
#         return context
#
#     def post(self, request):
#         name = request.POST.get("name")
#         desc = request.POST.get("desc")
#         image = request.FILES.get("image")
#         price = request.POST.get("price")
#         try:
#             category = Category.objects.get(id=request.POST.get("category"))
#         except ValueError:
#             category = None
#
#         Product.objects.create(
#             name=name,
#             desc=desc,
#             image=image,
#             category=category,
#             price=price,
#         )
#         return self.render_to_response(super().get_context_data())

# def homepage(request):
#     category_list = Category.objects.all()
#     if request.method == "POST":
#         name = request.POST.get("name")
#         desc = request.POST.get("desc")
#         image = request.FILES.get("image")
#         price = request.POST.get("price")
#         try:
#             category = Category.objects.get(id=request.POST.get("category"))
#         except ValueError:
#             category = None
#
#         Product.objects.create(
#             name=name,
#             desc=desc,
#             image=image,
#             category=category,
#             price=price,
#         )
#     context = {
#         'product_list': Product.objects.all(),
#         'catalog_list': category_list,
#         'title': 'Главная',
#     }
#     return render(request, 'catalog/homepage.html', context)
