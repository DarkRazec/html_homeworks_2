from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, VersionForm, VersionUpdateForm
from catalog.models import Product, Contact, Category, Version


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        try:
            version = Version.objects.filter(product=self.get_object(), is_active=True).first
        except Version.DoesNotExist:
            version = None
        context_data['version'] = version
        context_data['title'] = f'Каталог: {self.get_object()}'
        return context_data


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"

    def get_success_url(self):
        return reverse_lazy('catalog:product_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionUpdateForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        context_data['category_list'] = Category.objects.all()
        context_data['title'] = f'Редактирование: {self.object}'
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:homepage')


class HomePageView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/homepage.html'
    extra_context = {
        'category_list': Category.objects.all(),
        'title': 'Главная',
    }
    success_url = reverse_lazy('catalog:homepage')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        context_data['product_list'] = Product.objects.all()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return super().form_invalid(form)


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
