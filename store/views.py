import sys
import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CartForm, DiscountForm
from .models import Product
from checkout import Checkout

# ---- HTML Checkout View ----
def checkout_page_view(request):
    cart_form = CartForm(request.POST or None)
    discount_form = DiscountForm(request.POST or None)
    total_price = None
    available_discounts = {}
    show_discounts = False

    if 'check_discounts' in request.POST and cart_form.is_valid():
        quantities = {
            "VOUCHER": cart_form.cleaned_data['voucher'],
            "TSHIRT": cart_form.cleaned_data['tshirt'],
            "MUG": cart_form.cleaned_data['mug']
        }
        checkout_system = Checkout(quantities, config_file="config.json")
        available_discounts = checkout_system.detect_discounts()
        show_discounts = True

    elif 'apply_discounts' in request.POST and cart_form.is_valid() and discount_form.is_valid():
        quantities = {
            "VOUCHER": cart_form.cleaned_data['voucher'],
            "TSHIRT": cart_form.cleaned_data['tshirt'],
            "MUG": cart_form.cleaned_data['mug']
        }
        checkout_system = Checkout(quantities, config_file="config.json")
        available_discounts = checkout_system.detect_discounts()
        selected_discounts = {
            "SWAG_PACK": discount_form.cleaned_data.get("swag", False),
            "TWO_FOR_ONE_VOUCHER": discount_form.cleaned_data.get("two_for_one_voucher", False),
            "BULK_TSHIRT": discount_form.cleaned_data.get("bulk_tshirt", False)
        }
        total_price = checkout_system.apply_discounts(selected_discounts)
        show_discounts = True

    return render(request, "store/checkout.html", {
        "cart_form": cart_form,
        "discount_form": discount_form,
        "available_discounts": available_discounts,
        "total_price": total_price,
        "show_discounts": show_discounts
    })


# ---- API Checkout View ----
@csrf_exempt
def checkout_api_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        quantities = data.get("quantities", {})
        if not isinstance(quantities, dict):
            return JsonResponse({"error": "Quantities must be a dictionary"}, status=400)

        checkout = Checkout(quantities)
        total = checkout.apply_discounts(checkout.detect_discounts())
        return JsonResponse({"total": total}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# ---- Add Product API ----
@csrf_exempt
def add_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate fields
        if not all(field in data for field in ["code", "name", "price"]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        product = Product.objects.create(
            code=data["code"],
            name=data["name"],
            price=data["price"]
        )
        return JsonResponse({"message": "Product created", "id": product.id}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# ---- Get Products API ----
@csrf_exempt
def get_products(request):
    if request.method == "GET":
        products = list(Product.objects.values())
        return JsonResponse(products, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)
