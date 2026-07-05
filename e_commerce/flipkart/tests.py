from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cart, Product


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

    def test_buy_now_uses_selected_quantity(self):
        user = get_user_model().objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpassword123',
            full_name='Buyer',
            mobile_no='9999999999',
        )
        product = Product.objects.create(
            name='Quantity Product',
            price=150.00,
            image='product_images/qty.png',
            stock=10,
            is_active=True,
        )

        self.client.force_login(user)
        response = self.client.post(
            reverse('buy_now', args=[product.id]),
            {'quantity': 3},
        )

        self.assertRedirects(response, reverse('checkout'))
        cart_item = Cart.objects.get(user=user, product=product)
        self.assertEqual(cart_item.quantity, 3)
