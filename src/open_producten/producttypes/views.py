from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from open_producten.producttypes.models import (
    Category,
    Field,
    Link,
    Price,
    ProductType,
    Question,
)
from open_producten.producttypes.serializers.category import CategorySerializer
from open_producten.producttypes.serializers.children import (
    FieldSerializer,
    LinkSerializer,
    PriceSerializer,
    QuestionSerializer,
)
from open_producten.producttypes.serializers.producttype import ProductTypeSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    lookup_url_kwarg = "id"


class ProductTypeChildViewSet(ModelViewSet):

    def get_product_type(self):
        return get_object_or_404(ProductType, id=self.kwargs["product_type_id"])

    def get_queryset(self):
        return self.queryset.filter(product_type=self.get_product_type())

    def perform_create(self, serializer):
        serializer.save(product_type=self.get_product_type())


class ProductTypeLinkViewSet(ProductTypeChildViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_url_kwarg = "link_id"


class ProductTypePriceViewSet(ProductTypeChildViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    lookup_url_kwarg = "price_id"


class ProductTypeFieldViewSet(ProductTypeChildViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    lookup_url_kwarg = "field_id"


class ProductTypeQuestionViewSet(ProductTypeChildViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = "id"


class CategoryChildViewSet(ModelViewSet):

    def get_category(self):
        return get_object_or_404(Category, id=self.kwargs["category_id"])

    def get_queryset(self):
        return self.queryset.filter(category=self.get_category())

    def perform_create(self, serializer):
        serializer.save(category=self.get_category())


class CategoryQuestionViewSet(CategoryChildViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"
