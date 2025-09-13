from django.test import TestCase
from store.models import Product
from checkout import Checkout


class CheckoutTestCase(TestCase):

    def setUp(self):
        """Setup initial products before each test"""
        Product.objects.create(code="VOUCHER", name="Cofi Voucher", price=5.00)
        Product.objects.create(code="TSHIRT", name="Cofi T-Shirt", price=20.00)
        Product.objects.create(code="MUG", name="Cofi Coffee Mug", price=7.50)

        self.quantities = {"VOUCHER": 0, "TSHIRT": 0, "MUG": 0}
        self.checkout = Checkout(self.quantities)

    def test_empty_cart_total_is_zero(self):
        """Empty cart should return total of 0"""
        self.assertEqual(self.checkout.apply_discounts({}), 0.00)

    def test_no_discounts_applied(self):
        """Cart with products that do not meet discount rules should return normal price"""
        self.checkout.scan("VOUCHER")
        self.checkout.scan("TSHIRT")
        self.assertEqual(self.checkout.total(), 25.00) 

    def test_partial_swag_bundle(self):
        """SWAG discount should not apply if one item is missing"""
        self.checkout.scan("VOUCHER")
        self.checkout.scan("TSHIRT")
        self.assertEqual(self.checkout.total(), 25.00)

    def test_empty_checkout_system(self):
        """Checkout should return 0 when no items are present"""
        empty_checkout = Checkout({})
        self.assertEqual(empty_checkout.apply_discounts(empty_checkout.detect_discounts()), 0.00)

    def test_two_for_one_voucher_promotion(self):
        """Two vouchers should cost 5"""
        quantities = {"VOUCHER": 2, "TSHIRT": 0, "MUG": 0}
        checkout = Checkout(quantities)
        self.assertEqual(checkout.apply_discounts(checkout.detect_discounts()), 5.00)

    def test_three_vouchers_should_cost_10(self):
        """Three vouchers → cost should be 10"""
        quantities = {"VOUCHER": 3, "TSHIRT": 0, "MUG": 0}
        checkout = Checkout(quantities)
        self.assertEqual(checkout.apply_discounts(checkout.detect_discounts()), 10.00)

    def test_bulk_tshirt_discount(self):
        """3 or more TSHIRTs → 19 each"""
        quantities = {"VOUCHER": 0, "TSHIRT": 3, "MUG": 0}
        checkout = Checkout(quantities)
        self.assertEqual(checkout.apply_discounts(checkout.detect_discounts()), 57.00)

    def test_swag_bundle_discount(self):
        """SWAG bundle → 25"""
        quantities = {"VOUCHER": 1, "TSHIRT": 1, "MUG": 1}
        checkout = Checkout(quantities)
        self.assertEqual(checkout.apply_discounts(checkout.detect_discounts()), 25.00)

    def test_mixed_scenario(self):
        """SWAG + two extra vouchers"""
        quantities = {"VOUCHER": 3, "TSHIRT": 1, "MUG": 1}
        checkout = Checkout(quantities)
        self.assertEqual(checkout.apply_discounts(checkout.detect_discounts()), 30.00)
