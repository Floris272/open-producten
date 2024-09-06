from open_producten.producttypes.models import Condition
from open_producten.utils.tests.cases import BaseApiTestCase
from open_producten.utils.tests.helpers import model_to_dict_with_id

from ..factories import ConditionFactory


def condition_to_dict(condition):
    return model_to_dict_with_id(condition)


class TestProductTypeCondition(BaseApiTestCase):

    def setUp(self):
        super().setUp()
        self.data = {
            "name": "test condition",
            "question": "?",
            "positive_text": "+",
            "negative_text": "-",
        }
        self.path = "/api/v1/conditions/"

    def _create_condition(self):
        return ConditionFactory.create()

    def test_read_condition_without_credentials_returns_error(self):
        self.client._credentials = {}
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_create_condition(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(Condition.objects.first().name, "test condition")

    def test_update_condition(self):
        condition = self._create_condition()

        data = self.data | {"name": "updated"}
        response = self.put(condition.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(Condition.objects.first().name, "updated")

    def test_partial_update_condition(self):
        condition = self._create_condition()

        data = {"name": "updated"}
        response = self.patch(condition.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(Condition.objects.first().name, "updated")

    def test_read_conditions(self):
        condition = self._create_condition()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [condition_to_dict(condition)])

    def test_read_condition(self):
        condition = self._create_condition()

        response = self.get(condition.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, condition_to_dict(condition))

    def test_delete_condition(self):
        condition = self._create_condition()
        response = self.delete(condition.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Condition.objects.count(), 0)
