from django.db import migrations

def seed(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Brand = apps.get_model('shop', 'Brand')
    BrandProfile = apps.get_model('shop', 'BrandProfile')
    Size = apps.get_model('shop', 'Size')
    Product = apps.get_model('shop', 'Product')
    brand = Brand.objects.create(name='WEARHOUSE', country='Россия')
    BrandProfile.objects.create(brand=brand, website='https://example.com/', description='Демонстрационный бренд повседневной одежды.')
    sizes = [Size.objects.create(name=name) for name in ['S', 'M', 'L', 'XL']]
    categories = {name: Category.objects.create(name=name) for name in ['Футболки', 'Худи', 'Брюки']}
    data = [
        ('Футболка Essential', 'Футболки', 1990, 'Молочный', 'tee', 'cream'),
        ('Худи Everyday', 'Худи', 4990, 'Шалфей', 'hoodie', 'sage'),
        ('Брюки Straight', 'Брюки', 4490, 'Графит', 'pants', 'charcoal'),
        ('Футболка Relaxed', 'Футболки', 2490, 'Терракота', 'tee', 'clay'),
        ('Худи Weekend', 'Худи', 5490, 'Песочный', 'hoodie', 'sand'),
        ('Брюки Wide', 'Брюки', 4990, 'Оливковый', 'pants', 'olive'),
    ]
    for name, category, price, color, kind, tone in data:
        product = Product.objects.create(name=name, category=categories[category], brand=brand, price=price, stock=10, color=color, kind=kind, tone=tone)
        product.sizes.set(sizes[:3])

class Migration(migrations.Migration):
    dependencies = [('shop', '0001_initial')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
