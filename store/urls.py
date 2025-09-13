
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_page_view, name='checkout_page'), 
    path('checkout/', views.checkout_api_view, name='checkout_api'), 
    path('add-product/', views.add_product, name='add_product'),
    path('get-products/', views.get_products, name='get_products'),
]
