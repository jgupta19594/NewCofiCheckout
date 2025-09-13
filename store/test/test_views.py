from django.test import TestCase, Client
from store.models import Product
import json


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        Product.objects.create(code="VOUCHER", name="Cofi Voucher", price=5.00)
        Product.objects.create(code="TSHIRT", name="Cofi T-Shirt", price=20.00)
        Product.objects.create(code="MUG", name="Cofi Coffee Mug", price=7.50)

 
    def test_add_product_success(self):
        response = self.client.post(
            "/add-product/",
            data=json.dumps({"code": "CAP", "name": "Cofi Cap", "price": 10.00}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_add_product_invalid_json(self):
        response = self.client.post("/add-product/", data="invalid-json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_add_product_missing_fields(self):
        response = self.client.post(
            "/add-product/",
            data=json.dumps({"code": "CAP"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_add_product_invalid_method(self):
        response = self.client.get("/add-product/")
        self.assertEqual(response.status_code, 400)

    
    def test_get_products_success(self):
        response = self.client.get("/get-products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_products_invalid_method(self):
        response = self.client.post("/get-products/")
        self.assertEqual(response.status_code, 400)

    
    def test_checkout_api_success(self):
        response = self.client.post(
            "/checkout/",
            data=json.dumps({"quantities": {"VOUCHER": 2, "TSHIRT": 3, "MUG": 1}}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())

    def test_checkout_api_invalid_json(self):
        response = self.client.post("/checkout/", data="invalid-json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_checkout_api_invalid_quantities_type(self):
        response = self.client.post(
            "/checkout/",
            data=json.dumps({"quantities": "invalid-type"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_checkout_api_invalid_method(self):
        response = self.client.get("/checkout/")
        self.assertEqual(response.status_code, 400)


