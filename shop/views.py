from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Category, Brand, BrandProfile, Size, Product
from .forms import CategoryForm, BrandForm, BrandProfileForm, SizeForm, ProductForm



def home(request):
    return render(request, 'shop/home.html', {'page': 'home', 'products': Product.objects.select_related('category')[:3]})


def catalog(request):
    category = request.GET.get('category', '')
    categories = list(Category.objects.values_list('name', flat=True))
    if category not in categories:
        category = ''
    products = Product.objects.select_related('category', 'brand').prefetch_related('sizes')
    if category:
        products = products.filter(category__name=category)
    return render(request, 'shop/catalog.html', {'page': 'catalog', 'products': products, 'categories': categories, 'selected': category})


def about(request):
    return render(request, 'shop/about.html', {'page': 'about'})

TABLES = {
    'categories': (Category, CategoryForm, 'Категории', ['ID', 'Название', 'Описание']),
    'brands': (Brand, BrandForm, 'Бренды', ['ID', 'Название', 'Страна']),
    'profiles': (BrandProfile, BrandProfileForm, 'Профили брендов', ['ID', 'Бренд', 'Сайт', 'Описание']),
    'sizes': (Size, SizeForm, 'Размеры', ['ID', 'Размер']),
    'products': (Product, ProductForm, 'Товары', ['ID', 'Название', 'Категория', 'Бренд', 'Размеры', 'Цена, ₽', 'Остаток', 'Цвет', 'Силуэт', 'Палитра']),
}

def database_table(request, table):
    model, form_class, title, columns = TABLES[table]
    form = form_class(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            form.save()
        messages.success(request, 'Запись успешно добавлена в базу данных.')
        return redirect('shop:' + table)
    records = model.objects.all()
    if table == 'products':
        records = records.select_related('category', 'brand').prefetch_related('sizes')
        rows = [[o.pk, o.name, o.category, o.brand, ', '.join(s.name for s in o.sizes.all()), o.price, o.stock, o.color, o.get_kind_display(), o.get_tone_display()] for o in records]
    elif table == 'profiles':
        rows = [[o.pk, o.brand, o.website, o.description] for o in records.select_related('brand')]
    elif table == 'categories':
        rows = [[o.pk, o.name, o.description or '—'] for o in records]
    elif table == 'brands':
        rows = [[o.pk, o.name, o.country] for o in records]
    else:
        rows = [[o.pk, o.name] for o in records]
    return render(request, f'shop/db/{table}.html', {'page': 'database', 'table': table, 'table_title': title, 'form': form, 'columns': columns, 'rows': rows})
