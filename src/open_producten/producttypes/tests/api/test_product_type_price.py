import datetime
from decimal import Decimal

from django.forms import model_to_dict

from freezegun import freeze_time

from open_producten.producttypes.models import Price, PriceOption, ProductType
from open_producten.producttypes.tests.factories import (
    PriceFactory,
    PriceOptionFactory,
    ProductTypeFactory,
)
from open_producten.utils.tests.test_cases import BaseApiTestCase


def price_to_dict(price):
    price_dict = model_to_dict(price, exclude=["product_type"]) | {"id": str(price.id)}
    price_dict["options"] = [model_to_dict(option) for option in price.options.all()]
    price_dict["valid_from"] = str(price_dict["valid_from"])

    return price_dict


@freeze_time("2024-01-01")
class TestProductTypePrice(BaseApiTestCase):

    def setUp(self):
        self.product_type = ProductTypeFactory()
        self.price_data = {"valid_from": datetime.date(2024, 1, 2)}
        self.endpoint = f"/api/v1/producttypes/{self.product_type.id}/prices/"

    def create_price(self):
        return PriceFactory.create(
            product_type=self.product_type, valid_from=datetime.date(2024, 1, 2)
        )

    def test_create_price(self):
        response = self.post(self.price_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(
            self.product_type.prices.first().valid_from, self.price_data["valid_from"]
        )

    def test_create_price_with_price_option(self):
        data = {
            "valid_from": datetime.date(2024, 1, 2),
            "options": [{"amount": "74.99", "description": "spoed"}],
        }

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(PriceOption.objects.count(), 1)
        self.assertEqual(
            self.product_type.prices.first().options.first().amount,
            Decimal("74.99"),
        )

    def test_update_price_removing_options(self):
        price = self.create_price()
        PriceOptionFactory.create(price=price)
        PriceOptionFactory.create(price=price)

        data = {
            "valid_from": price.valid_from,
            "options": [],
        }

        response = self.put(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(PriceOption.objects.count(), 0)

    def test_update_price_updating_and_removing_options(self):
        price = self.create_price()
        option_to_be_updated = PriceOptionFactory.create(price=price)
        PriceOptionFactory.create(price=price)

        data = {
            "valid_from": price.valid_from,
            "options": [
                {
                    "id": option_to_be_updated.id,
                    "amount": "20",
                    "description": option_to_be_updated.description,
                }
            ],
        }

        response = self.put(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(PriceOption.objects.count(), 1)
        self.assertEqual(PriceOption.objects.first().amount, Decimal("20"))

    def test_update_price_creating_and_deleting_options(self):
        price = self.create_price()
        PriceOptionFactory.create(price=price)

        data = {
            "valid_from": price.valid_from,
            "options": [{"amount": "20", "description": "test"}],
        }

        response = self.put(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(PriceOption.objects.count(), 1)
        self.assertEqual(PriceOption.objects.first().amount, Decimal("20"))

    def test_exception_when_option_not_part_of_price(self):
        price = self.create_price()

        option = PriceOptionFactory.create(price=PriceFactory.create())

        data = {
            "valid_from": price.valid_from,
            "options": [
                {"id": option.id, "amount": "20", "description": option.description}
            ],
        }

        response = self.put(price.id, data)

        self.assertEqual(response.status_code, 400)

    def test_partial_update_price(self):
        price = self.create_price()
        PriceOptionFactory.create(price=price)

        data = {"valid_from": datetime.date(2024, 1, 4)}

        response = self.patch(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(
            ProductType.objects.first().prices.first().valid_from,
            datetime.date(2024, 1, 4),
        )
        self.assertEqual(PriceOption.objects.count(), 1)

    def test_partial_update_price_updating_and_removing_options(self):
        price = self.create_price()
        option_to_be_updated = PriceOptionFactory.create(price=price)
        PriceOptionFactory.create(price=price)

        data = {
            "valid_from": price.valid_from,
            "options": [
                {
                    "id": option_to_be_updated.id,
                    "amount": "20",
                    "description": option_to_be_updated.description,
                }
            ],
        }

        response = self.patch(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(PriceOption.objects.count(), 1)
        self.assertEqual(PriceOption.objects.first().amount, Decimal("20"))

    def test_partial_update_price_creating_and_deleting_options(self):
        price = self.create_price()
        PriceOptionFactory.create(price=price)

        data = {
            "valid_from": datetime.date(2024, 1, 4),
            "options": [{"amount": "20", "description": "test"}],
        }

        response = self.patch(price.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(
            ProductType.objects.first().prices.first().valid_from,
            datetime.date(2024, 1, 4),
        )
        self.assertEqual(PriceOption.objects.count(), 1)
        self.assertEqual(PriceOption.objects.first().description, "test")

    def test_read_prices(self):
        price = self.create_price()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [price_to_dict(price)])

    def test_read_price(self):
        price = self.create_price()

        response = self.get(price.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, price_to_dict(price))

    def test_delete_price(self):
        price = self.create_price()
        response = self.delete(price.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Price.objects.count(), 0)
        self.assertEqual(PriceOption.objects.count(), 0)
