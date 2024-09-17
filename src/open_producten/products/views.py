from rest_framework.viewsets import ModelViewSet

from open_producten.products.models import Product
from open_producten.products.serializers.product import (
    ProductSerializer,
    ProductUpdateSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_url_field = "id"

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return ProductUpdateSerializer
        return ProductSerializer
