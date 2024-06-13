from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version

BAD_WORDS = ('казино',
             'криптовалюта',
             'крипта',
             'биржа',
             'дешево',
             'бесплатно',
             'обман',
             'полиция',
             'радар')


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'desc', 'author', 'is_published', 'category')

    @classmethod
    def cleaning(cls, data):
        for word in BAD_WORDS:
            if word in data:
                raise forms.ValidationError('Введено запрещенное слово')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        self.cleaning(cleaned_data)
        return cleaned_data

    def clean_desc(self):
        cleaned_data = self.cleaned_data.get('desc')
        self.cleaning(cleaned_data)
        return cleaned_data


class ModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'author')


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class VersionUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def clean_is_active(self):
        cleaned_data = self.cleaned_data.get('is_active')
        product = self.cleaned_data.get('product')
        versions = Version.objects.filter(product=product, is_active=True).first()
        if versions and cleaned_data:
            raise forms.ValidationError('Активная версия уже существует')
        return cleaned_data
