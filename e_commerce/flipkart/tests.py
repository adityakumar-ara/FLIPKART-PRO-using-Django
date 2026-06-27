from django.test import TestCase
from django.urls import reverse

from .models import Product


class HomePageTests(TestCase):
    def test_home_page_shows_only_owner_selected_top_products(self):
        owner_selected = Product.objects.create(
            name='Owner Picked Product',
            price=199.99,
            image='product_images/test.png',
            is_active=True,
            is_owner_selected=True,
        )
        Product.objects.create(
            name='Regular Product',
            price=99.99,
            image='product_images/test2.png',
            is_active=True,
            is_owner_selected=False,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(owner_selected, response.context['top_products'])
        self.assertEqual(len(response.context['top_products']), 1)
