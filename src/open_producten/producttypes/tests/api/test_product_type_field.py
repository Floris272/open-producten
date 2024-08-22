from django.forms import model_to_dict

from open_producten.producttypes.models import Field, ProductType
from open_producten.producttypes.tests.factories import FieldFactory, ProductTypeFactory
from open_producten.utils.tests.test_cases import BaseApiTestCase


def field_to_dict(field):
    return model_to_dict(field, exclude=["product_type"]) | {"id": str(field.id)}


class TestProductTypeField(BaseApiTestCase):

    def setUp(self):
        self.product_type = ProductTypeFactory.create()
        self.data = {"name": "test field", "description": "test", "type": "textfield"}
        self.endpoint = f"/api/v1/producttypes/{self.product_type.id}/fields/"

    def create_field(self):
        return FieldFactory.create(product_type=self.product_type)

    def test_create_field(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "test field")

    def test_update_field(self):
        field = self.create_field()

        data = self.data | {"name": "updated"}
        response = self.put(field.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "updated")

    def test_partial_update_field(self):
        field = self.create_field()

        data = {"name": "updated"}
        response = self.patch(field.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().fields.first().name, "updated")

    def test_read_fields(self):
        field = self.create_field()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [field_to_dict(field)])

    def test_read_field(self):
        field = self.create_field()

        response = self.get(field.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, field_to_dict(field))

    def test_delete_field(self):
        field = self.create_field()
        response = self.delete(field.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Field.objects.count(), 0)
