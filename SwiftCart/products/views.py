# products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from accounts.permissions import IsSalesManager, IsAdmin

# Product list view accessible by customers, sales managers, and admins
class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        product_data = ProductSerializer(products, many=True).data
        return Response(product_data)

# Sales Manager view for creating or editing products
class ProductManageView(APIView):
    permission_classes = [IsSalesManager | IsAdmin]

    def post(self, request):
        data = request.data
        product = Product.objects.create(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            description=data['description'],
        )
        return Response({"message": "Product created successfully!"})
