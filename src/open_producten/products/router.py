from django.urls import include, path

from rest_framework_nested.routers import DefaultRouter

from open_producten.products.views import ProductViewSet

ProductRouter = DefaultRouter()
ProductRouter.register("products", ProductViewSet, basename="product")

product_urlpatterns = [
    path("", include(ProductRouter.urls)),
]
