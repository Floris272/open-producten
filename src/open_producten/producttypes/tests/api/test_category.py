from open_producten.producttypes.models import Category
from open_producten.producttypes.tests.factories import (
    CategoryFactory,
    ProductTypeFactory,
)
from open_producten.utils.tests.test_cases import BaseApiTestCase


class TestCategoryViewSet(BaseApiTestCase):

    def setUp(self):
        self.data = {
            "name": "test-category",
            "parent_category": None,
        }
        self.endpoint = "/api/v1/categories/"

    def test_create_minimal_category(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_category_with_parent(self):
        parent = CategoryFactory.create()
        data = self.data | {"parent_category": parent.id}

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(
            Category.objects.get(id=response.data["id"]).get_parent(), parent
        )

    def test_create_category_with_product_type(self):
        product_type = ProductTypeFactory.create()
        data = self.data | {"product_type_ids": [product_type.id]}

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().product_types.first(), product_type)

    def test_change_parent(self):
        new_parent = CategoryFactory.create()
        category = CategoryFactory.create()

        data = self.data | {"parent_category": new_parent.id}
        response = self.put(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(), new_parent)
