from django import forms

from goods.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product(self):
        cleaned_data = self.cleaned_data['product']

        if ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
            'радар',) in cleaned_data:
            raise forms.ValidationError('Данный продукт запрещен к добавлению')

        return cleaned_data


class SubjectForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
