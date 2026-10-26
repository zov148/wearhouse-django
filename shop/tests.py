from django.test import TestCase
from django.urls import reverse


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
        self.assertTrue(all(p['category'] == 'Худи' for p in response.context['products']))

    def test_unknown_category_shows_all(self):
        response = self.client.get(reverse('shop:catalog'), {'category': 'unknown'})
        self.assertEqual(len(response.context['products']), 6)
