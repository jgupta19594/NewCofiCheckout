from django.test import TestCase
from store.models import Product


class ProductModelTest(TestCase):
    def test_str_representation(self):
        product = Product.objects.create(code="VOUCHER", name="Cofi Voucher", price=5.00)
        self.assertEqual(str(product), "Cofi Voucher")
