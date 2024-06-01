from django import forms
from django.forms import BooleanField
from django.forms.utils import ErrorList

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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at',)

    def cleaning(self, data, data_name):
        for word in BAD_WORDS:
            if word in data:
                self._errors[data_name] = ErrorList()
                self._errors[data_name].append('Введено запрещенное слово')
                break

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        self.cleaning(cleaned_data, 'name')
        return cleaned_data

    def clean_desc(self):
        cleaned_data = self.cleaned_data.get('desc')
        self.cleaning(cleaned_data, 'desc')
        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        exclude = ('product',)

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"
