from django.db import transaction

from rest_framework import serializers

from open_producten.utils.serializers import build_array_duplicates_error_message

from ..models import Category, Condition, ProductType, Tag, UniformProductName
from .children import (
    ConditionSerializer,
    FieldSerializer,
    FileSerializer,
    LinkSerializer,
    PriceSerializer,
    QuestionSerializer,
    TagSerializer,
    UniformProductNameSerializer,
)


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("path", "depth", "numchild")


class ProductTypeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        default=[],
        write_only=True,
        source="tags",
    )

    related_product_types = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ProductType.objects.all(), default=[]
    )

    uniform_product_name_id = serializers.PrimaryKeyRelatedField(
        queryset=UniformProductName.objects.all(),
        write_only=True,
        source="uniform_product_name",
    )

    uniform_product_name = UniformProductNameSerializer(read_only=True)

    conditions = ConditionSerializer(many=True, read_only=True)
    condition_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Condition.objects.all(),
        default=[],
        source="conditions",
    )

    categories = SimpleCategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source="categories",
    )

    questions = QuestionSerializer(many=True, read_only=True)
    fields = FieldSerializer(many=True, read_only=True)
    prices = PriceSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ProductType
        fields = "__all__"

    def validate_category_ids(self, category_ids):
        if len(category_ids) == 0:
            raise serializers.ValidationError("At least one category is required")
        return category_ids

    def _handle_relations(
        self, instance, related_product_types, categories, tags, conditions
    ):
        errors = dict()
        if related_product_types is not None:
            build_array_duplicates_error_message(
                related_product_types, "related_product_types", errors
            )
            instance.related_product_types.set(related_product_types)
        if categories is not None:
            build_array_duplicates_error_message(categories, "category_ids", errors)
            instance.categories.set(categories)
        if tags is not None:
            build_array_duplicates_error_message(tags, "tag_ids", errors)
            instance.tags.set(tags)
        if conditions is not None:
            build_array_duplicates_error_message(conditions, "condition_ids", errors)
            instance.conditions.set(conditions)

        if errors:
            raise serializers.ValidationError(errors)

    @transaction.atomic()
    def create(self, validated_data):
        related_product_types = validated_data.pop("related_product_types")
        categories = validated_data.pop("categories")
        conditions = validated_data.pop("conditions")
        tags = validated_data.pop("tags")

        product_type = ProductType.objects.create(**validated_data)

        self._handle_relations(
            product_type, related_product_types, categories, tags, conditions
        )
        product_type.save()

        return product_type

    @transaction.atomic()
    def update(self, instance, validated_data):
        related_product_types = validated_data.pop("related_product_types", None)
        categories = validated_data.pop("categories", None)
        conditions = validated_data.pop("conditions", None)
        tags = validated_data.pop("tags", None)

        instance = super().update(instance, validated_data)
        self._handle_relations(
            instance, related_product_types, categories, tags, conditions
        )

        instance.save()

        return instance


class ProductTypeCurrentPriceSerializer(serializers.ModelSerializer):
    upl_uri = serializers.ReadOnlyField(source="uniform_product_name.url")
    upl_name = serializers.ReadOnlyField(source="uniform_product_name.name")
    current_price = PriceSerializer(allow_null=True)

    class Meta:
        model = ProductType
        fields = ("id", "name", "upl_name", "upl_uri", "current_price")
