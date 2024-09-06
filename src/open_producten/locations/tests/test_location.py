from django.test import TestCase

from .factories import LocationFactory


class TestLocation(TestCase):

    def setUp(self):
        self.location = LocationFactory.create(
            street="Keizersgracht",
            house_number="117",
            postcode="1015 CJ",
            city="Amsterdam",
        )

    def test_address(self):
        self.assertEqual(self.location.address, "Keizersgracht 117, 1015CJ Amsterdam")
