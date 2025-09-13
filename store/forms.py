from django import forms

class CartForm(forms.Form):
    voucher = forms.IntegerField(min_value=0, initial=0, label="VOUCHER")
    tshirt = forms.IntegerField(min_value=0, initial=0, label="TSHIRT")
    mug = forms.IntegerField(min_value=0, initial=0, label="MUG")

class DiscountForm(forms.Form):
    swag = forms.BooleanField(required=False, label="SWAG PACK")
    two_for_one_voucher = forms.BooleanField(required=False, label="2-FOR-1 VOUCHER")
    bulk_tshirt = forms.BooleanField(required=False, label="BULK TSHIRT")
tshirt = forms.BooleanField(required=False, label="BULK TSHIRT")
