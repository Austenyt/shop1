from django import forms

from goods.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                            'полиция', 'радар']

        for word in prohibited_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f"Слово '{word}' недопустимо для использования в названии.")
        return cleaned_data

    def clean_description(self):
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                            'полиция', 'радар']
        description = self.cleaned_data['description']
        for word in prohibited_words:
            if word in description.lower():
                raise forms.ValidationError(f"Слово '{word}' недопустимо для использования в описании.")
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
