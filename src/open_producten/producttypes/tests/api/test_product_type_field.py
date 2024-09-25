from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from open_producten.producttypes.models import Field, ProductType
from open_producten.producttypes.tests.factories import FieldFactory, ProductTypeFactory
from open_producten.utils.tests.cases import BaseApiTestCase
from open_producten.utils.tests.helpers import model_to_dict_with_id


def field_to_dict(field):
    return model_to_dict_with_id(field, exclude=["product_type"])


class TestProductTypeField(BaseApiTestCase):

    def setUp(self):
        super().setUp()
        self.product_type = ProductTypeFactory.create()
        self.data = {"name": "test field", "description": "test", "type": "textfield"}
        self.path = f"/api/v1/producttypes/{self.product_type.id}/fields/"

    def _create_field(self):
        return FieldFactory.create(product_type=self.product_type)

    def test_read_field_without_credentials_returns_error(self):
        response = APIClient().get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_create_field(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "test field")

    def test_create_normal_field_with_choices_returns_error(self):
        response = self.post(self.data | {"choices": ["a", "b"]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "choices": [
                    ErrorDetail(string="textfield cannot have choices", code="invalid")
                ]
            },
        )

    def test_create_choice_field_without_choices_returns_error(self):
        response = self.post(self.data | {"type": "select"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "choices": [
                    ErrorDetail(
                        string="Choices are required for select", code="invalid"
                    )
                ]
            },
        )

    def test_update_field(self):
        field = self._create_field()

        data = self.data | {"name": "updated"}
        response = self.put(field.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "updated")

    def test_partial_update_field(self):
        field = self._create_field()

        data = {"name": "updated"}
        response = self.patch(field.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "updated")

    def test_partial_update_change_choices(self):
        field = FieldFactory.create(
            product_type=self.product_type, type="select", choices=["a", "b"]
        )

        data = {"choices": ["a"]}
        response = self.patch(field.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().choices, ["a"])

    def test_read_fields(self):
        field = self._create_field()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], [field_to_dict(field)])

    def test_read_field(self):
        field = self._create_field()

        response = self.get(field.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, field_to_dict(field))

    def test_delete_field(self):
        field = self._create_field()
        response = self.delete(field.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Field.objects.count(), 0)
