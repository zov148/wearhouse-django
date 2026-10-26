from django import forms
from .models import Category, Brand, BrandProfile, Size, Product

class ShopModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = 'Заполните это поле.'
        if 'sizes' in self.fields:
            self.fields['sizes'].help_text = 'Можно выбрать несколько размеров.'

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if self._meta.model is Size:
            name = name.upper()
        existing = self._meta.model.objects.all()
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if any(value.casefold() == name.casefold() for value in existing.values_list('name', flat=True)):
            raise forms.ValidationError('Запись с таким названием уже существует.')
        return name

class CategoryForm(ShopModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

class BrandForm(ShopModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'country']

class BrandProfileForm(ShopModelForm):
    class Meta:
        model = BrandProfile
        fields = ['brand', 'website', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}
        error_messages = {'brand': {'unique': 'У этого бренда уже есть профиль. Выберите другой бренд.'}}

class SizeForm(ShopModelForm):
    class Meta:
        model = Size
        fields = ['name']
        help_texts = {'name': 'XXS, XS, S, M, L, XL, XXL или XXXL; регистр не важен.'}

class ProductForm(ShopModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'sizes', 'price', 'stock', 'color', 'kind', 'tone']
        widgets = {'sizes': forms.CheckboxSelectMultiple()}
