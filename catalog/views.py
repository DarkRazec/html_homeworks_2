from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, VersionForm, VersionUpdateForm, ModeratorForm
from catalog.models import Product, Contact, Version
from catalog.services import get_category_list


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


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    template_name = "catalog/product_update.html"

    def get_success_url(self):
        return reverse_lazy('catalog:product_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionUpdateForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        context['category_list'] = get_category_list()
        context['title'] = f'Редактирование: {self.object}'
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('catalog.set_published') and user.has_perm('catalog.change_category'):
            return ModeratorForm
        elif user == self.object.author:
            return self.form_class
        return PermissionDenied


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:homepage')


class HomePageView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/homepage.html'
    permission_required = 'catalog.delete_product'
    extra_context = {
        'title': 'Главная',
    }
    success_url = reverse_lazy('catalog:homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        context['product_list'] = Product.objects.all()
        context['category_list'] = get_category_list()
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save()
            self.object.author = self.request.user
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
