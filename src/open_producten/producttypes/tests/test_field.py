from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import FieldTypes
from .factories import FieldFactory


class TestField(TestCase):

    def test_choice_field_requires_choices(self):
        field = FieldFactory.build(type=FieldTypes.RADIO)

        with self.assertRaises(ValidationError):
            field.clean()

        field = FieldFactory.build(type=FieldTypes.SELECT)

        with self.assertRaises(ValidationError):
            field.clean()

        field = FieldFactory.build(type=FieldTypes.SELECT_BOXES)

        with self.assertRaises(ValidationError):
            field.clean()

    def test_normal_field_cannot_have_choices(self):
        field = FieldFactory.build(type=FieldTypes.TEXTFIELD, choices=["a", "b"])

        with self.assertRaises(ValidationError):
            field.clean()
