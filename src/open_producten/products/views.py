from rest_framework.viewsets import ModelViewSet

from open_producten.products.models import Product
from open_producten.products.serializers.product import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_field = "id"
