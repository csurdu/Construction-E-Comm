from decimal import Decimal

from django.test import TestCase

from .forms import OrderForm
from .models import Item


class OrderFormTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Cement Bag",
            description="50kg bag",
            price=Decimal("12.50"),
            quantity=10,
        )

    def test_order_reduces_inventory(self):
        form = OrderForm(
            data={
                "customer_name": "Alex Customer",
                "customer_email": "alex@example.com",
                "item": self.item.pk,
                "quantity": 3,
            }
        )
        self.assertTrue(form.is_valid())
        order = form.create_order()
        self.item.refresh_from_db()

        self.assertIsNotNone(order.pk)
        self.assertEqual(self.item.quantity, 7)

    def test_prevents_overselling(self):
        form = OrderForm(
            data={
                "customer_name": "Alex Customer",
                "customer_email": "alex@example.com",
                "item": self.item.pk,
                "quantity": 25,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Only", form.errors["quantity"][0])
