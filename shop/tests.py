from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import Category, Brand, BrandProfile, Size, Product


class ShopPagesTests(TestCase):
    def test_pages_and_navigation(self):
        for name in ['home', 'catalog', 'about']:
            response = self.client.get(reverse('shop:' + name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<header', html=False)
            self.assertContains(response, '<footer', html=False)
            for target in ['home', 'catalog', 'about']:
                self.assertContains(response, 'href="' + reverse('shop:' + target) + '"')

    def test_catalog_filter(self):
        response = self.client.get(reverse('shop:catalog'), {'category': 'Худи'})
        self.assertEqual(len(response.context['products']), 2)
        self.assertTrue(all(p.category.name == 'Худи' for p in response.context['products']))

    def test_shared_includes_and_external_assets(self):
        for name in ['home', 'catalog', 'about']:
            response = self.client.get(reverse('shop:' + name))
            self.assertTemplateUsed(response, 'shop/base.html')
            self.assertTemplateUsed(response, 'shop/includes/header.html')
            self.assertTemplateUsed(response, 'shop/includes/footer.html')
            self.assertContains(response, '<header', count=1)
            self.assertContains(response, '<footer', count=1)
            self.assertContains(response, '/static/shop/styles.css', count=1)
            self.assertContains(response, '/static/shop/script.js', count=1)
            self.assertNotContains(response, '<style')
            self.assertNotContains(response, 'onclick=')

    def test_unknown_category_shows_all(self):
        response = self.client.get(reverse('shop:catalog'), {'category': 'unknown'})
        self.assertEqual(len(response.context['products']), 6)

class DatabaseTests(TestCase):
    def test_table_pages(self):
        for name in ['categories', 'brands', 'profiles', 'sizes', 'products']:
            response = self.client.get(reverse('shop:' + name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'shop/db/{name}.html')
            self.assertContains(response, 'csrfmiddlewaretoken')
            self.assertContains(response, 'Записи в базе')

    def test_create_records_in_all_five_tables(self):
        self.assertEqual(self.client.post(reverse('shop:categories'), {'name': 'Куртки'}).status_code, 302)
        self.assertEqual(self.client.post(reverse('shop:brands'), {'name': 'Новый бренд', 'country': 'Россия'}).status_code, 302)
        brand = Brand.objects.get(name='Новый бренд')
        self.assertEqual(self.client.post(reverse('shop:profiles'), {'brand': brand.pk, 'website': 'https://example.org/', 'description': 'Подробное описание нового бренда.'}).status_code, 302)
        self.assertEqual(self.client.post(reverse('shop:sizes'), {'name': 'xxl'}).status_code, 302)
        sizes = list(Size.objects.filter(name__in=['M', 'XXL']).values_list('pk', flat=True))
        response = self.client.post(reverse('shop:products'), {'name': 'Куртка Test', 'category': Category.objects.get(name='Куртки').pk, 'brand': brand.pk, 'sizes': sizes, 'price': '7500.50', 'stock': '5', 'color': 'Чёрный', 'kind': 'hoodie', 'tone': 'charcoal'})
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(name='Куртка Test')
        self.assertEqual(product.sizes.count(), 2)
        self.assertEqual(brand.profile.website, 'https://example.org/')
        self.assertContains(self.client.get(reverse('shop:catalog')), product.name)

    def test_invalid_price_and_stock_not_saved(self):
        count = Product.objects.count()
        response = self.client.post(reverse('shop:products'), {'name': 'Невалидный товар', 'category': Category.objects.first().pk, 'brand': Brand.objects.first().pk, 'sizes': [Size.objects.first().pk], 'price': '-5', 'stock': '-1', 'color': 'Белый', 'kind': 'tee', 'tone': 'cream'})
        self.assertFormError(response.context['form'], 'price', 'Убедитесь, что это значение больше либо равно 0.01.')
        self.assertTrue(response.context['form'].errors.get('stock'))
        self.assertEqual(Product.objects.count(), count)

    def test_duplicate_profile_rejected(self):
        count = BrandProfile.objects.count()
        response = self.client.post(reverse('shop:profiles'), {'brand': Brand.objects.first().pk, 'website': 'https://example.org/', 'description': 'Другое подробное описание.'})
        self.assertContains(response, 'У этого бренда уже есть профиль.')
        self.assertEqual(BrandProfile.objects.count(), count)

    def test_required_url_duplicate_and_size_validation(self):
        for url, data in [('categories', {'name': ''}), ('categories', {'name': 'футболки'}), ('sizes', {'name': '42'}), ('profiles', {'brand': Brand.objects.first().pk, 'website': 'bad', 'description': 'коротко'})]:
            response = self.client.post(reverse('shop:' + url), data)
            self.assertContains(response, 'Запись не сохранена.')
            self.assertTrue(response.context['form'].errors)

    def test_foreign_keys_and_many_to_many(self):
        brand = Brand.objects.first()
        self.assertGreater(brand.products.count(), 1)
        size = Size.objects.get(name='M')
        self.assertGreater(size.products.count(), 1)
        self.assertGreater(Product.objects.first().sizes.count(), 1)

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        url = reverse('shop:categories')
        self.assertEqual(client.post(url, {'name': 'Без токена'}).status_code, 403)
        client.get(url)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post(url, {'name': 'С токеном', 'csrfmiddlewaretoken': token}).status_code, 302)
