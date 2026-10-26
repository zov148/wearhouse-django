from django.shortcuts import render

PRODUCTS = [
    {'name': 'Футболка Essential', 'category': 'Футболки', 'price': '1 990', 'color': 'Молочный', 'kind': 'tee', 'tone': 'cream'},
    {'name': 'Худи Everyday', 'category': 'Худи', 'price': '4 990', 'color': 'Шалфей', 'kind': 'hoodie', 'tone': 'sage'},
    {'name': 'Брюки Straight', 'category': 'Брюки', 'price': '4 490', 'color': 'Графит', 'kind': 'pants', 'tone': 'charcoal'},
    {'name': 'Футболка Relaxed', 'category': 'Футболки', 'price': '2 490', 'color': 'Терракота', 'kind': 'tee', 'tone': 'clay'},
    {'name': 'Худи Weekend', 'category': 'Худи', 'price': '5 490', 'color': 'Песочный', 'kind': 'hoodie', 'tone': 'sand'},
    {'name': 'Брюки Wide', 'category': 'Брюки', 'price': '4 990', 'color': 'Оливковый', 'kind': 'pants', 'tone': 'olive'},
]


def home(request):
    return render(request, 'shop/home.html', {'page': 'home', 'products': PRODUCTS[:3]})


def catalog(request):
    category = request.GET.get('category', '')
    categories = ['Футболки', 'Худи', 'Брюки']
    if category not in categories:
        category = ''
    products = [p for p in PRODUCTS if not category or p['category'] == category]
    return render(request, 'shop/catalog.html', {'page': 'catalog', 'products': products, 'categories': categories, 'selected': category})


def about(request):
    return render(request, 'shop/about.html', {'page': 'about'})
