import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

import pytz

from open_producten.producttypes.models import Field, FieldTypes
from open_producten.producttypes.tests.factories import FieldFactory

from .factories import DataFactory


class TestData(TestCase):

    def test_parse_number(self):
        field = FieldFactory.create(type=FieldTypes.NUMBER)

        data = DataFactory.create(field=field, value="5")
        self.assertEqual(data.parse(), 5)

    def test_parse_checkbox(self):
        field = FieldFactory.create(type=FieldTypes.CHECKBOX)

        data = DataFactory.create(field=field, value="true")
        self.assertEqual(data.parse(), True)

        data = DataFactory.create(field=field, value="false")
        self.assertEqual(data.parse(), False)

    def test_parse_date(self):
        field = FieldFactory.create(type=FieldTypes.DATE)

        data = DataFactory.create(field=field, value="2024-07-16")
        self.assertEqual(data.parse(), datetime.date(2024, 7, 16))

    def test_parse_datetime(self):
        field = FieldFactory.create(type=FieldTypes.DATETIME)

        data = DataFactory.create(field=field, value="2024-07-11T12:04:03+02:00")
        tz = pytz.timezone("Europe/Amsterdam")

        self.assertEqual(
            data.parse(), tz.localize(datetime.datetime(2024, 7, 11, 12, 4, 3))
        )

    def test_parse_time(self):
        field = FieldFactory.create(type=FieldTypes.TIME)

        data = DataFactory.create(field=field, value="12:33:01")
        self.assertEqual(data.parse(), datetime.time(12, 33, 1))

    def test_parse_map(self):
        field = FieldFactory.create(type=FieldTypes.MAP)

        data = DataFactory.create(
            field=field, value="52.13309377014838,5.339086446962994"
        )
        self.assertEqual(data.parse(), ["52.13309377014838", "5.339086446962994"])

    def test_parse_select(self):
        field = FieldFactory.create(type=FieldTypes.SELECT)

        data = DataFactory.create(field=field, value="abc,def")
        self.assertEqual(data.parse(), ["abc", "def"])

    def _subtest_invalid_data_values(self, field: Field, *invalid_values):
        for invalid_value in invalid_values:
            with self.subTest(f"{invalid_value} should raise an error"):
                with self.assertRaises(ValidationError):
                    DataFactory.build(field=field, value=invalid_value).clean()

    def _subtest_valid_data_values(self, field: Field, *valid_values):
        for valid_value in valid_values:
            with self.subTest(f"{valid_value} should not raise an error"):
                DataFactory.build(field=field, value=valid_value).clean()

    def test_clean_bsn_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.BSN)
        self._subtest_invalid_data_values(field, "1234", "abc", "123456789")

    def test_clean_bsn_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.BSN)
        self._subtest_valid_data_values(field, "111222333")

    def test_clean_checkbox_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.CHECKBOX)
        self._subtest_invalid_data_values(field, "1234", True)

    def test_clean_checkbox_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.CHECKBOX)
        self._subtest_valid_data_values(field, "true", "false")

    def test_clean_cosign_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.COSIGN)
        self._subtest_invalid_data_values(field, "abcde", "abcde@", "abcde@gmail.")

    def test_clean_cosign_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.COSIGN)
        self._subtest_valid_data_values(field, "abcde@gmail.com")

    def test_clean_currency_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.CURRENCY)
        self._subtest_invalid_data_values(field, "abcde", "123a")

    def test_clean_currency_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.CURRENCY)
        self._subtest_valid_data_values(field, "123124", "123124,12")

    def test_clean_date_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.DATE)
        self._subtest_invalid_data_values(field, "abc", "20240101", "2024-13-01")

    def test_clean_date_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.DATE)
        self._subtest_valid_data_values(field, "2024-01-01")

    def test_clean_datetime_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.DATETIME)
        self._subtest_invalid_data_values(field, "abc", "20241001", "2023-13-01")

    def test_clean_datetime_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.DATETIME)
        self._subtest_valid_data_values(field, "2024-01-01T13:00:00+02:00")

    def test_clean_email_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.EMAIL)
        self._subtest_invalid_data_values(field, "abcde", "xyz@", "abcde@gmail.")

    def test_clean_email_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.EMAIL)
        self._subtest_valid_data_values(field, "abcde@gmail.com")

    def test_clean_iban_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.IBAN)
        self._subtest_invalid_data_values(field, "0001234567", "NL10INGB0001234567")

    def test_clean_iban_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.IBAN)
        self._subtest_valid_data_values(field, "NL20INGB0001234567")

    def test_clean_license_plate_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.LICENSE_PLATE)
        self._subtest_invalid_data_values(field, "abcde", "abc123ad")

    def test_clean_license_plate_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.LICENSE_PLATE)
        self._subtest_valid_data_values(field, "123-AA-1")

    def test_clean_map_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.MAP)
        self._subtest_invalid_data_values(field, "abcde", "42, 21")

    def test_clean_map_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.MAP)
        self._subtest_valid_data_values(field, "42,12", "42.1294323,12.9283498")

    def test_clean_number_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.NUMBER)
        self._subtest_invalid_data_values(field, "abcde")

    def test_clean_number_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.NUMBER)
        self._subtest_valid_data_values(field, "42.12", "42.1294323")

    def test_clean_phone_number_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.PHONE_NUMBER)
        self._subtest_invalid_data_values(field, "abcde")

    def test_clean_phone_number_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.PHONE_NUMBER)
        self._subtest_valid_data_values(field, "0612165228", "+31 6 12 16 52 28")

    def test_clean_postcode_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.POSTCODE)
        self._subtest_invalid_data_values(field, "AB 3123", "0334 AA")

    def test_clean_postcode_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.POSTCODE)
        self._subtest_valid_data_values(field, "3441ER", "3441 ER")

    def test_clean_radio_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.RADIO, choices=["a", "b"])
        self._subtest_invalid_data_values(field, "d")

    def test_clean_radio_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.RADIO, choices=["a", "b"])
        self._subtest_valid_data_values(field, "a", "b")

    def test_clean_select_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.SELECT, choices=["a", "b"])
        self._subtest_invalid_data_values(field, "", "d,", "d", "a,d")

    def test_clean_select_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.SELECT, choices=["a", "b"])
        self._subtest_valid_data_values(field, "a", "a,b")

    def test_clean_select_boxes_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.SELECT_BOXES, choices=["a", "b"])
        self._subtest_invalid_data_values(
            field, ")(", '{"a": true}', '{"a": true, "d": true}'
        )

    def test_clean_select_boxes_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.SELECT_BOXES, choices=["a", "b"])
        self._subtest_valid_data_values(field, '{"a": true, "b": true}')

    def test_clean_signature_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.SIGNATURE)
        self._subtest_invalid_data_values(field, "signature")

    def test_clean_signature_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.SIGNATURE)
        self._subtest_valid_data_values(field, "data:image/png;base64,A812EEAa")

    def test_clean_time_raises_on_invalid_value(self):
        field = FieldFactory.create(type=FieldTypes.TIME)
        self._subtest_invalid_data_values(field, "abc", "120302")

    def test_clean_time_validates_on_valid_value(self):
        field = FieldFactory.create(type=FieldTypes.TIME)
        self._subtest_valid_data_values(field, "12:00:00")
