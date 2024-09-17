from open_producten.producttypes.models import TagType
from open_producten.utils.tests.cases import BaseApiTestCase
from open_producten.utils.tests.helpers import model_to_dict_with_id

from ..factories import TagTypeFactory


def tag_type_to_dict(tag_type):
    return model_to_dict_with_id(tag_type)


class TestProductTypeTagType(BaseApiTestCase):

    def setUp(self):
        self.data = {"name": "test tag_type"}
        self.path = "/api/v1/tagtypes/"

    def create_tag(self):
        return TagTypeFactory.create()

    def test_create_tag(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(TagType.objects.count(), 1)
        self.assertEqual(TagType.objects.first().name, "test tag_type")

    def test_update_tag(self):
        tag_type = self.create_tag()

        data = self.data | {"name": "updated"}
        response = self.put(tag_type.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TagType.objects.count(), 1)
        self.assertEqual(TagType.objects.first().name, "updated")

    def test_partial_update_tag(self):
        tag_type = self.create_tag()

        data = {"name": "updated"}
        response = self.patch(tag_type.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TagType.objects.count(), 1)
        self.assertEqual(TagType.objects.first().name, "updated")

    def test_read_tag_types(self):
        tag_type = self.create_tag()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [tag_type_to_dict(tag_type)])

    def test_read_tag(self):
        tag_type = self.create_tag()

        response = self.get(tag_type.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, tag_type_to_dict(tag_type))

    def test_delete_tag(self):
        tag_type = self.create_tag()
        response = self.delete(tag_type.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TagType.objects.count(), 0)
