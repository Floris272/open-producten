from django.forms import model_to_dict

from open_producten.producttypes.models import Category, Question
from open_producten.producttypes.tests.factories import CategoryFactory, QuestionFactory
from open_producten.utils.tests.test_cases import BaseApiTestCase


def question_to_dict(question):
    return model_to_dict(question, exclude=["product_type", "category"]) | {
        "id": str(question.id)
    }


class TestCategoryQuestion(BaseApiTestCase):

    def setUp(self):
        self.category = CategoryFactory.create()
        self.data = {"question": "18?", "answer": "eligible"}
        self.endpoint = f"/api/v1/categories/{self.category.id}/questions/"

    def create_question(self):
        return QuestionFactory.create(category=self.category)

    def test_create_question(self):
        response = self.post(self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(self.category.questions.first().question, "18?")

    def test_update_question(self):
        question = self.create_question()

        data = self.data | {"question": "21?"}
        response = self.put(question.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Category.objects.first().questions.first().question, "21?")

    def test_partial_update_question(self):
        question = self.create_question()

        data = {"question": "21?"}
        response = self.patch(question.id, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Category.objects.first().questions.first().question, "21?")

    def test_read_questions(self):
        question = self.create_question()

        response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [question_to_dict(question)])

    def test_read_question(self):
        question = self.create_question()

        response = self.get(question.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, question_to_dict(question))

    def test_delete_question(self):
        question = self.create_question()
        response = self.delete(question.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Question.objects.count(), 0)
