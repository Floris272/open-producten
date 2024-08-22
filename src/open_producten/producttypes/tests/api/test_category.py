from django.forms import model_to_dict

from open_producten.producttypes.models import Category, Link
from open_producten.producttypes.tests.factories import (
    CategoryFactory,
    ProductTypeFactory,
    QuestionFactory,
)
from open_producten.utils.tests.test_cases import BaseApiTestCase


def category_to_dict(category):
    category_dict = model_to_dict(category, exclude=("path", "depth", "numchild")) | {
        "id": str(category.id)
    }
    category_dict["questions"] = [
        model_to_dict(question) for question in category.questions.all()
    ]
    category_dict["product_types"] = [
        model_to_dict(product_type) for product_type in category.product_types.all()
    ]
    category_dict["created_on"] = str(category.created_on.astimezone().isoformat())
    category_dict["updated_on"] = str(category.updated_on.astimezone().isoformat())
    return category_dict


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

    def test_update_change_from_root_to_parent(self):
        new_parent = CategoryFactory.create()
        category = CategoryFactory.create()

        data = self.data | {"parent_category": new_parent.id}
        response = self.put(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(), new_parent)

    def test_update_change_from_parent_to_root(self):
        parent_category = CategoryFactory.create()
        category = parent_category.add_child(name="test-category")

        data = self.data | {"parent_category": None}
        response = self.put(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(), None)

    def test_update_change_from_parent_to_parent(self):
        parent_category = CategoryFactory.create()
        category = parent_category.add_child(name="test-category")

        new_parent_category = CategoryFactory.create()

        data = self.data | {"parent_category": new_parent_category.id}
        response = self.put(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(update=True), new_parent_category)

    def test_partial_update(self):
        parent_category = CategoryFactory.create()
        category = parent_category.add_child(name="test-category")

        data = {"name": "updated"}
        response = self.patch(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.name, "updated")
        self.assertEqual(category.get_parent(), parent_category)

    def test_partial_update_change_parent(self):
        parent_category = CategoryFactory.create()
        category = parent_category.add_child(name="test-category")

        new_parent_category = CategoryFactory.create()

        data = {"parent_category": new_parent_category.id}
        response = self.patch(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(update=True), new_parent_category)

    def test_partial_update_change_parent_to_root(self):
        parent_category = CategoryFactory.create()
        category = parent_category.add_child(name="test-category")

        data = {"parent_category": None}
        response = self.patch(category.id, data)

        category.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.get_parent(update=True), None)

    def test_read_categories(self):
        category = CategoryFactory.create()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [category_to_dict(category)])

    def test_read_category(self):
        category = CategoryFactory.create()

        response = self.get(category.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, category_to_dict(category))

    def test_delete_category(self):
        category = CategoryFactory.create()
        QuestionFactory.create(category=category)

        response = self.delete(category.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Link.objects.count(), 0)
