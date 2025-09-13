
# import json
# from collections import Counter

# class Checkout:
#     def __init__(self, quantities, config_file="config.json"):
#         with open(config_file) as f:
#             config = json.load(f)
#         self.products = config["products"]
#         self.discounts = config["discounts"]
#         self.items = Counter(quantities)

#     def detect_discounts(self):
#         """Detect available discounts based on current items"""
#         discounts = {}
#         if "SWAG_PACK" in self.discounts:
#             num_swag = min([self.items[i] for i in self.discounts["SWAG_PACK"]["items"]])
#             if num_swag > 0:
#                 discounts["SWAG_PACK"] = num_swag
#         if "TWO_FOR_ONE_VOUCHER" in self.discounts:
#             qty = self.items.get("VOUCHER", 0)
#             if qty >= 2:
#                 discounts["TWO_FOR_ONE_VOUCHER"] = qty // 2
#         if "BULK_TSHIRT" in self.discounts:
#             qty = self.items.get("TSHIRT", 0)
#             min_qty = self.discounts["BULK_TSHIRT"]["min_quantity"]
#             if qty >= min_qty:
#                 discounts["BULK_TSHIRT"] = qty

#         return discounts

#     def apply_discounts(self, selected):
#         """Apply discounts in proper order: SWAG → 2-for-1 → Bulk → Remaining"""
#         total = 0.0
#         items = self.items.copy()
#         if selected.get("SWAG_PACK") and "SWAG_PACK" in self.discounts:
#             num_swag = min([items[i] for i in self.discounts["SWAG_PACK"]["items"]])
#             total += num_swag * self.discounts["SWAG_PACK"]["price"]
#             for i in self.discounts["SWAG_PACK"]["items"]:
#                 items[i] -= num_swag
#         if selected.get("TWO_FOR_ONE_VOUCHER") and "TWO_FOR_ONE_VOUCHER" in self.discounts:
#             qty = items.get("VOUCHER", 0)
#             if qty > 0:
#                 total += (qty // 2 + qty % 2) * self.products["VOUCHER"]["price"]
#                 items["VOUCHER"] = 0 
#         if selected.get("BULK_TSHIRT") and "BULK_TSHIRT" in self.discounts:
#             qty = items.get("TSHIRT", 0)
#             min_qty = self.discounts["BULK_TSHIRT"]["min_quantity"]
#             if qty >= min_qty:
#                 total += qty * self.discounts["BULK_TSHIRT"]["new_price"]
#                 items["TSHIRT"] = 0
#         for k, v in items.items():
#             total += v * self.products[k]["price"]

#         return round(total, 2)

import json
from collections import Counter

class Checkout:
    def __init__(self, quantities, config_file="config.json"):
        # Load products and discounts from config file
        with open(config_file) as f:
            config = json.load(f)
        self.products = config["products"]
        self.discounts = config["discounts"]

        # Initialize cart with given quantities
        self.items = Counter(quantities)

    def scan(self, sku):
        """Add a product to the cart by SKU"""
        if sku not in self.products:
            raise ValueError(f"Invalid SKU: {sku}")
        self.items[sku] += 1

    def detect_discounts(self):
        """Detect available discounts based on current items"""
        discounts = {}

        # SWAG PACK discount
        if "SWAG_PACK" in self.discounts:
            num_swag = min([self.items[i] for i in self.discounts["SWAG_PACK"]["items"]])
            if num_swag > 0:
                discounts["SWAG_PACK"] = num_swag

        # 2-for-1 Voucher discount
        if "TWO_FOR_ONE_VOUCHER" in self.discounts:
            qty = self.items.get("VOUCHER", 0)
            if qty >= 2:
                discounts["TWO_FOR_ONE_VOUCHER"] = qty // 2

        # Bulk T-Shirt discount
        if "BULK_TSHIRT" in self.discounts:
            qty = self.items.get("TSHIRT", 0)
            min_qty = self.discounts["BULK_TSHIRT"]["min_quantity"]
            if qty >= min_qty:
                discounts["BULK_TSHIRT"] = qty

        return discounts

    def apply_discounts(self, selected):
        """Apply discounts in proper order: SWAG → 2-for-1 → Bulk → Remaining"""
        total = 0.0
        items = self.items.copy()

        # 1. Apply SWAG Pack
        if selected.get("SWAG_PACK") and "SWAG_PACK" in self.discounts:
            num_swag = min([items[i] for i in self.discounts["SWAG_PACK"]["items"]])
            total += num_swag * self.discounts["SWAG_PACK"]["price"]
            for i in self.discounts["SWAG_PACK"]["items"]:
                items[i] -= num_swag

        # 2. Apply 2-for-1 Voucher
        if selected.get("TWO_FOR_ONE_VOUCHER") and "TWO_FOR_ONE_VOUCHER" in self.discounts:
            qty = items.get("VOUCHER", 0)
            if qty > 0:
                total += (qty // 2 + qty % 2) * self.products["VOUCHER"]["price"]
                items["VOUCHER"] = 0 

        # 3. Apply Bulk T-Shirt discount
        if selected.get("BULK_TSHIRT") and "BULK_TSHIRT" in self.discounts:
            qty = items.get("TSHIRT", 0)
            min_qty = self.discounts["BULK_TSHIRT"]["min_quantity"]
            if qty >= min_qty:
                total += qty * self.discounts["BULK_TSHIRT"]["new_price"]
                items["TSHIRT"] = 0

        # 4. Add remaining items without discount
        for k, v in items.items():
            total += v * self.products[k]["price"]

        return round(total, 2)

    def total(self):
        """Calculate the final total automatically"""
        detected_discounts = self.detect_discounts()
        return self.apply_discounts(detected_discounts)


















