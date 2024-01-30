from django import forms

from goods.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class ProductForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def clean_product(self):
#         cleaned_data = self.cleaned_data['product']
#
#         if ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
#             'радар',) in cleaned_data:
#             raise forms.ValidationError('Данный продукт запрещен к добавлению')
#
#         return cleaned_data

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
                raise forms.ValidationError(f"The word '{word}' is not allowed in the name.")
        return cleaned_data

    def clean_description(self):
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                            'полиция', 'радар']
        description = self.cleaned_data['description']
        for word in prohibited_words:
            if word in description.lower():
                raise forms.ValidationError(f"The word '{word}' is not allowed in the description.")
        return description


