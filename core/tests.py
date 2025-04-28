from django.test import TestCase
from .models import Customer, Order

class CustomerOrderTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", code="TST001")
    
    def test_create_order(self):
        order = Order.objects.create(customer=self.customer, item="Test Item", amount=10.50)
        self.assertEqual(order.customer.name, "Test Customer")
        self.assertEqual(order.item, "Test Item")
        self.assertEqual(float(order.amount), 10.50)

# Coverage check
# Run tests with coverage:
# coverage run manage.py test
# coverage report -m
