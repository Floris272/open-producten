from django.db import transaction

from rest_framework import serializers

from open_producten.producttypes.models import Category, ProductType
from open_producten.utils.serializers import check_for_duplicates_in_array

from .children import QuestionSerializer, UniformProductNameSerializer


class SimpleProductTypeSerializer(serializers.ModelSerializer):
    uniform_product_name = UniformProductNameSerializer()

    class Meta:
        model = ProductType
        exclude = ("categories", "conditions", "tags", "related_product_types")


class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        write_only=True,
    )
    product_types = SimpleProductTypeSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    product_type_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ProductType.objects.all(),
        default=[],
        write_only=True,
        source="product_types",
    )

    class Meta:
        model = Category
        exclude = ("path", "depth", "numchild")

    def _handle_relations(self, instance, product_types):
        errors = dict()
        if product_types is not None:
            check_for_duplicates_in_array(product_types, "product_type_ids", errors)
            instance.product_types.set(product_types)

        if errors:
            raise serializers.ValidationError(errors)

    @transaction.atomic()
    def create(self, validated_data):
        product_types = validated_data.pop("product_types")
        parent_category = validated_data.pop("parent_category")

        if parent_category:
            category = parent_category.add_child(**validated_data)
        else:
            category = Category.add_root(**validated_data)

        self._handle_relations(category, product_types)
        category.save()

        return category

    @transaction.atomic()
    def update(self, instance, validated_data):
        product_types = validated_data.pop("product_types", None)
        parent_category = validated_data.pop(
            "parent_category", "ignore"
        )  # None is a valid value

        if parent_category != "ignore":
            instance_parent = instance.get_parent()
            if parent_category is None and instance_parent is not None:
                last_root = Category.get_last_root_node()
                instance.move(last_root, "last-sibling")

            elif parent_category != instance_parent:
                instance.move(parent_category, "last-child")

            instance.refresh_from_db()

        instance = super().update(instance, validated_data)
        self._handle_relations(instance, product_types)
        instance.save()
        return instance
