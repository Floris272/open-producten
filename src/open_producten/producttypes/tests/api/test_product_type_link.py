from django.forms import model_to_dict

from open_producten.producttypes.models import Link, ProductType
from open_producten.utils.tests.cases import BaseApiTestCase

from ..factories import LinkFactory, ProductTypeFactory


def link_to_dict(link):
    return model_to_dict(link, exclude=["product_type"]) | {"id": str(link.id)}


class TestProductTypeLink(BaseApiTestCase):

    def setUp(self):
        self.product_type = ProductTypeFactory.create()
        self.data = {"name": "test link", "url": "https://www.google.com"}
        self.path = f"/api/v1/producttypes/{self.product_type.id}/links/"

    def create_link(self):
        return LinkFactory.create(product_type=self.product_type)

    def test_create_link(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().links.first().name, "test link")

    def test_update_link(self):
        link = self.create_link()

        data = self.data | {"name": "updated"}
        response = self.put(link.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().links.first().name, "updated")

    def test_partial_update_link(self):
        link = self.create_link()

        data = {"name": "updated"}
        response = self.patch(link.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().links.first().name, "updated")

    def test_read_links(self):
        link = self.create_link()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [link_to_dict(link)])

    def test_read_link(self):
        link = self.create_link()

        response = self.get(link.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, link_to_dict(link))

    def test_delete_link(self):
        link = self.create_link()
        response = self.delete(link.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Link.objects.count(), 0)
