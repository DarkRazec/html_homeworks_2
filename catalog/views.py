from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, DeleteView

from catalog.models import Product, Contact, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:homepage')


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
