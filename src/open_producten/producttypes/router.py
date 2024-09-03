from django.urls import include, path

from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

from open_producten.producttypes.views import (
    CategoryQuestionViewSet,
    CategoryViewSet,
    ConditionViewSet,
    ProductTypeFieldViewSet,
    ProductTypeLinkViewSet,
    ProductTypePriceViewSet,
    ProductTypeQuestionViewSet,
    ProductTypeViewSet,
    TagTypeViewSet,
    TagViewSet,
)

ProductTypesRouter = DefaultRouter()
ProductTypesRouter.register("producttypes", ProductTypeViewSet, basename="producttype")

ProductTypesLinkRouter = NestedSimpleRouter(
    ProductTypesRouter, "producttypes", lookup="product_type"
)
ProductTypesLinkRouter.register(
    r"links", ProductTypeLinkViewSet, basename="producttype-link"
)

ProductTypesPriceRouter = NestedSimpleRouter(
    ProductTypesRouter, "producttypes", lookup="product_type"
)
ProductTypesPriceRouter.register(
    r"prices", ProductTypePriceViewSet, basename="producttype-price"
)

ProductTypesQuestionRouter = NestedSimpleRouter(
    ProductTypesRouter, "producttypes", lookup="product_type"
)
ProductTypesQuestionRouter.register(
    r"questions", ProductTypeQuestionViewSet, basename="producttype-question"
)

ProductTypesFieldRouter = NestedSimpleRouter(
    ProductTypesRouter, "producttypes", lookup="product_type"
)
ProductTypesFieldRouter.register(
    r"fields", ProductTypeFieldViewSet, basename="producttype-field"
)

ProductTypesRouter.register("categories", CategoryViewSet, basename="category")

CategoriesQuestionRouter = NestedSimpleRouter(
    ProductTypesRouter, "categories", lookup="category"
)
CategoriesQuestionRouter.register(
    r"questions", CategoryQuestionViewSet, basename="category-question"
)

ProductTypesRouter.register("conditions", ConditionViewSet, basename="condition")
ProductTypesRouter.register("tags", TagViewSet, basename="tag")
ProductTypesRouter.register("tagtypes", TagTypeViewSet, basename="tagtype")

product_type_urlpatterns = [
    path("", include(ProductTypesRouter.urls)),
    path("", include(ProductTypesLinkRouter.urls)),
    path("", include(ProductTypesPriceRouter.urls)),
    path("", include(ProductTypesQuestionRouter.urls)),
    path("", include(ProductTypesFieldRouter.urls)),
    path("", include(CategoriesQuestionRouter.urls)),
]
