import datetime

from django.forms import model_to_dict
from freezegun import freeze_time
from rest_framework.exceptions import ErrorDetail

from open_producten.products.models import Product, Data
from open_producten.products.tests.factories import ProductFactory
from open_producten.producttypes.models import FieldTypes
from open_producten.producttypes.tests.factories import ProductTypeFactory, FieldFactory
from open_producten.utils.tests.cases import BaseApiTestCase


def product_to_dict(product):
    product_dict = model_to_dict(product, exclude=["product_type"]) | {"id": str(product.id)}
    product_dict["start_date"] = str(product_dict["start_date"])
    product_dict["data"] = [model_to_dict(data) for data in product.data.all()]
    product_dict["end_date"] = str(product_dict["end_date"])
    product_dict["created_on"] = str(product.created_on.astimezone().isoformat())
    product_dict["updated_on"] = str(product.updated_on.astimezone().isoformat())

    product_dict["product_type"] = model_to_dict(product.product_type) | {"id": str(product.product_type.id)}
    product_dict["product_type"]["uniform_product_name"] = model_to_dict(product.product_type.uniform_product_name) | {
        "id": str(product.product_type.uniform_product_name.id)}

    product_dict["product_type"]["created_on"] = str(product.product_type.created_on.astimezone().isoformat())
    product_dict["product_type"]["updated_on"] = str(product.product_type.updated_on.astimezone().isoformat())
    return product_dict


@freeze_time("2024-01-01")
class TestProduct(BaseApiTestCase):

    def setUp(self):
        self.product_type = ProductTypeFactory.create()
        self.data = {"product_type_id": self.product_type.id, "bsn": "111222333",
                     "start_date": datetime.date(2024, 1, 2), "end_date": datetime.date(2024, 12, 31), "data": []}
        self.path = "/api/v1/products/"

    def create_product(self):
        return ProductFactory.create()

    def test_create_product(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_without_required_fields_returns_error(self):
        product_type = ProductTypeFactory.create()
        FieldFactory.create(product_type=product_type, type=FieldTypes.TEXTFIELD, is_required=True)

        data = self.data | {"product_type_id": product_type.id}

        response = self.post(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "data": [
                    ErrorDetail(
                        string="Missing required fields: field 0",
                        code="invalid",
                    )
                ]
            },
        )

    def test_create_product_without_non_required_fields_returns_error(self):
        product_type = ProductTypeFactory.create()
        FieldFactory.create(product_type=product_type, type=FieldTypes.TEXTFIELD, is_required=False)

        data = self.data | {"product_type_id": product_type.id}

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_with_data_for_required_field_returns_error(self):
        product_type = ProductTypeFactory.create()
        field = FieldFactory.create(product_type=product_type, type=FieldTypes.TEXTFIELD, is_required=True)

        data = self.data | {"product_type_id": product_type.id, "data": [{
            "field_id": field.id,
            "value": "abc"
        }]}

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Data.objects.count(), 1)

    def test_create_product_with_data_for_unrequired_field_returns_error(self):
        product_type = ProductTypeFactory.create()
        field = FieldFactory.create(product_type=product_type, type=FieldTypes.TEXTFIELD, is_required=False)

        data = self.data | {"product_type_id": product_type.id, "data": [{
            "field_id": field.id,
            "value": "abc"
        }]}

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Data.objects.count(), 1)

    def test_create_product_with_wrong_data_for_field_returns_error(self):
        product_type = ProductTypeFactory.create()
        field = FieldFactory.create(product_type=product_type, type=FieldTypes.NUMBER, is_required=True)

        data = self.data | {"product_type_id": product_type.id, "data": [{
            "field_id": field.id,
            "value": "abc"
        }]}

        response = self.post(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "data": [
                    ErrorDetail(
                        string="Data at index 0: ['invalid number']",  # TODO
                        code="invalid",
                    )
                ]
            },
        )

    def test_create_product_with_data_for_field_not_part_of_product_type_returns_error(self):
        product_type = ProductTypeFactory.create()
        field = FieldFactory.create(type=FieldTypes.TEXTFIELD, is_required=True)

        data = self.data | {"product_type_id": product_type.id, "data": [{
            "field_id": field.id,
            "value": "abc"
        }]}

        response = self.post(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "data": [
                    ErrorDetail(
                        string="field field 0 is not part of product type 2",  # TODO
                        code="invalid",
                    )
                ]
            },
        )

    def test_update_product(self):
        product = self.create_product()

        data = self.data | {"end_date": datetime.date(2025, 12, 31)}
        response = self.put(product.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    def test_partial_update_product(self):
        product = self.create_product()

        data = {"end_date": datetime.date(2025, 12, 31)}
        response = self.patch(product.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    def test_read_products(self):
        product = self.create_product()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [product_to_dict(product)])

    def test_read_product(self):
        product = self.create_product()

        response = self.get(product.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, product_to_dict(product))

        self.assertEqual(response.data, product_to_dict(product))

    def test_delete_product(self):
        product = self.create_product()
        response = self.delete(product.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)
