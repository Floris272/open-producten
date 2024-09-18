from rest_framework.test import APIClient

from open_producten.producttypes.models import Tag
from open_producten.utils.tests.cases import BaseApiTestCase
from open_producten.utils.tests.helpers import model_to_dict_with_id

from ..factories import TagFactory, TagTypeFactory


def tag_to_dict(tag):
    tag_dict = model_to_dict_with_id(tag)
    tag_dict["type"] = model_to_dict_with_id(tag.type)
    return tag_dict


class TestProductTypeTag(BaseApiTestCase):

    def setUp(self):
        super().setUp()
        self.tag_type = TagTypeFactory()
        self.data = {"name": "test tag", "type_id": self.tag_type.id}
        self.path = "/api/v1/tags/"

    def test_read_tag_without_credentials_returns_error(self):
        response = APIClient().get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_create_tag(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, "test tag")

    def test_update_tag(self):
        tag = TagFactory.create()

        data = self.data | {"name": "updated"}
        response = self.put(tag.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, "updated")

    def test_partial_update_tag(self):
        tag = TagFactory.create()

        data = {"name": "updated"}
        response = self.patch(tag.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, "updated")

    def test_read_tags(self):
        tag = TagFactory.create()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [tag_to_dict(tag)])

    def test_read_tag(self):
        tag = TagFactory.create()

        response = self.get(tag.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, tag_to_dict(tag))

    def test_delete_tag(self):
        tag = TagFactory.create()
        response = self.delete(tag.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Tag.objects.count(), 0)
