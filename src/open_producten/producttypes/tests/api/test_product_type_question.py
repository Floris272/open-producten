from django.forms import model_to_dict

from rest_framework.test import APIClient

from open_producten.producttypes.models import ProductType, Question
from open_producten.producttypes.tests.factories import (
    ProductTypeFactory,
    QuestionFactory,
)
from open_producten.utils.tests.cases import BaseApiTestCase


def question_to_dict(question):
    return model_to_dict(question, exclude=["product_type", "category"]) | {
        "id": str(question.id)
    }


class TestProductTypeQuestion(BaseApiTestCase):

    def setUp(self):
        super().setUp()
        self.product_type = ProductTypeFactory.create()
        self.data = {"question": "18?", "answer": "eligible"}
        self.path = f"/api/v1/producttypes/{self.product_type.id}/questions/"

    def _create_question(self):
        return QuestionFactory.create(product_type=self.product_type)

    def test_read_question_without_credentials_returns_error(self):
        response = APIClient().get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_create_question(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(self.product_type.questions.first().question, "18?")

    def test_update_question(self):
        question = self._create_question()

        data = self.data | {"question": "21?"}
        response = self.put(question.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().questions.first().question, "21?")

    def test_partial_update_question(self):
        question = self._create_question()

        data = {"question": "21?"}
        response = self.patch(question.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(ProductType.objects.first().questions.first().question, "21?")

    def test_read_questions(self):
        question = self._create_question()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], [question_to_dict(question)])

    def test_read_question(self):
        question = self._create_question()

        response = self.get(question.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, question_to_dict(question))

    def test_delete_question(self):
        question = self._create_question()
        response = self.delete(question.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Question.objects.count(), 0)
