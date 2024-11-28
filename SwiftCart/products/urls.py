# products/urls.py
from django.urls import path
from .views import ProductListView, ProductManageView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('manage/', ProductManageView.as_view(), name='product_manage'),
]
