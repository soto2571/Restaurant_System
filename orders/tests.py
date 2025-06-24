from django.test import TestCase
from .models import Table, Account, OrderNote

class OrderModelTest(TestCase):
    def test_create_order_note(self):
        table = Table.objects.create(number=1)
        account = Account.objects.create(table=table, customer_name="John")
        order = OrderNote.objects.create(account=account, item="Pizza")
        self.assertEqual(order.status, "pending")
