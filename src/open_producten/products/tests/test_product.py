from django.core.exceptions import ValidationError
from django.test import TestCase

from open_producten.producttypes.tests.factories import ProductTypeFactory

from .factories import ProductFactory


class TestProduct(TestCase):

    def setUp(self):
        self.product_type = ProductTypeFactory.create()

    def test_bsn_validation_raises_on_invalid_value(self):
        invalid_values = [
            "123",  # min length
            "12345678910",  # max length
            "abcdefghi",  # regex
            "192837465",  # 11 check
        ]
        for value in invalid_values:
            with self.subTest(f"{value} should raise an error"):
                with self.assertRaises(ValidationError):
                    ProductFactory.build(
                        bsn=value, product_type=self.product_type
                    ).full_clean()

    def test_bsn_validation_validates_on_valid_value(self):
        ProductFactory.build(
            bsn="111222333", product_type=self.product_type
        ).full_clean()

    def test_kvk_validation_raises_on_invalid_value(self):
        invalid_values = [
            "1234",  # min length
            "123456789",  # max length
            "test",  # regex
        ]
        for value in invalid_values:
            with self.subTest(f"{value} should raise an error"):
                with self.assertRaises(ValidationError):
                    ProductFactory.build(
                        kvk=value, product_type=self.product_type
                    ).full_clean()

    def test_kvk_validation_validates_on_valid_value(self):
        ProductFactory.build(
            kvk="11122333", product_type=self.product_type
        ).full_clean()

    def test_bsn_or_kvk_required(self):
        product = ProductFactory.build(product_type=self.product_type)

        with self.assertRaises(ValidationError):
            product.clean()

        ProductFactory.build(
            bsn="111222333", product_type=self.product_type
        ).full_clean()
        ProductFactory.build(
            kvk="11122233", product_type=self.product_type
        ).full_clean()
