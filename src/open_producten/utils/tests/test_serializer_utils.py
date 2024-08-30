from unittest import TestCase

from ..serializers import check_for_duplicates_in_array


class Dummy:

    def __init__(self, id):
        self.id = id


class TestCheckForDuplicates(TestCase):

    def setUp(self):
        self.object_a = Dummy("a")
        self.object_b = Dummy("b")

    def test_check_duplicates_should_raise_when_list_has_duplicate_object(self):
        errors = dict()
        object_list = [self.object_a, self.object_b, self.object_b]

        check_for_duplicates_in_array(object_list, "test", errors)

        self.assertEqual(errors, {"test": f"Duplicate Dummy id: b at index {2}"})

    def test_check_duplicates_should_no_raise_when_list_has_unique_values(self):
        errors = dict()
        object_list = [self.object_a, self.object_b]

        check_for_duplicates_in_array(object_list, "test", errors)
