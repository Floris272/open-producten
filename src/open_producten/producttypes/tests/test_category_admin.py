from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.test import TestCase

from open_producten.utils.tests.helpers import build_formset_data

from ..admin.category import CategoryAdmin, CategoryAdminForm, CategoryAdminFormSet
from ..models import Category
from .factories import CategoryFactory


def create_form(data, instance=None):
    return CategoryAdminForm(
        instance=instance,
        data=data,
    )


class TestCategoryAdminForm(TestCase):

    def setUp(self):
        self.data = {
            "name": "test",
            "_position": "first-child",
            "path": "00010001",
            "numchild": 1,
            "depth": 1,
        }

    def test_parent_nodes_must_be_published_when_publishing_child(self):
        parent = CategoryFactory.create(published=False)
        data = self.data | {"published": True, "_ref_node_id": parent.id}

        form = create_form(data)

        self.assertEquals(
            form.non_field_errors(),
            ["Parent nodes have to be published in order to publish a child."],
        )

        parent.published = True
        parent.save()

        form = create_form(data)
        self.assertEquals(form.errors, {})

    def test_parent_nodes_cannot_be_unpublished_with_published_children(self):
        parent = CategoryFactory.create(published=False)
        parent.add_child(**{"name": "child", "published": True})
        data = {"published": False, "_ref_node_id": None}

        form = create_form(data, parent)

        self.assertEquals(
            form.non_field_errors(),
            ["Parent nodes cannot be unpublished if they have published children."],
        )


class TestCategoryAdminFormSet(TestCase):

    def setUp(self):
        self.formset = modelformset_factory(
            model=Category,
            formset=CategoryAdminFormSet,
            fields=CategoryAdmin.list_editable,
        )

        self.parent = Category.add_root(**{"name": "parent", "published": False})
        self.child = self.parent.add_child(**{"name": "child", "published": True})

    def test_parent_nodes_cannot_be_unpublished_with_published_children(self):
        data = build_formset_data(
            "form",
            {
                "id": self.parent.id,  # published off
            },
            {"id": self.child.id, "published": "on"},
        )

        object_formset = self.formset(data)

        with self.assertRaises(ValidationError):
            object_formset.clean()
