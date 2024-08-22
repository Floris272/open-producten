from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import (
    Condition,
    Field,
    File,
    Link,
    Price,
    PriceOption,
    Question,
    Tag,
    TagType,
    UniformProductName,
)


class PriceOptionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = PriceOption
        exclude = ("price",)


class PriceSerializer(serializers.ModelSerializer):
    options = PriceOptionSerializer(many=True, default=[])

    class Meta:
        model = Price
        exclude = ("product_type",)

    @transaction.atomic()
    def create(self, validated_data):
        options = validated_data.pop("options")
        product_type = validated_data.pop("product_type")

        price = Price.objects.create(**validated_data, product_type=product_type)

        for option in options:
            PriceOption.objects.create(price=price, **option)

        return price

    @transaction.atomic()
    def update(self, instance, validated_data):
        options = validated_data.pop("options", None)
        price = super().update(instance, validated_data)
        current_option_ids = list(price.options.values_list("id", flat=True))

        if options is not None:
            for option in options:
                option_id = option.pop("id", None)
                if option_id is None:
                    PriceOption.objects.create(price=price, **option)

                elif option_id in current_option_ids:
                    existing_option = PriceOption.objects.get(id=option_id)
                    existing_option.amount = option["amount"]
                    existing_option.description = option["description"]
                    existing_option.save()
                    current_option_ids.remove(option_id)

                else:
                    raise ValidationError(
                        f"Price option id {option_id} is not part of to price object."
                    )

            PriceOption.objects.filter(id__in=current_option_ids).delete()

        return price


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        exclude = ("product_type",)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ("id", "product_type")


class TagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagType
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    type = TagTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=TagType.objects.all(), source="type"
    )

    class Meta:
        model = Tag
        fields = "__all__"


class UpnSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniformProductName
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ("category", "product_type")


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ("product_type",)
