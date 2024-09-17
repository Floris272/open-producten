from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from open_producten.products.models import Data, Product
from open_producten.producttypes.models import Field, ProductType
from open_producten.producttypes.serializers.category import SimpleProductTypeSerializer
from open_producten.producttypes.serializers.children import FieldSerializer
from open_producten.utils.serializers import model_to_dict_with_related_ids


class DataSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=True)
    field_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Field.objects.all(), source="field"
    )

    class Meta:
        model = Data
        exclude = ("product",)


class BaseProductSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        without_data = attrs.copy()
        without_data.pop("data", None)

        if self.partial:
            all_attrs = model_to_dict_with_related_ids(self.instance) | without_data
        else:
            all_attrs = without_data

        instance = Product(**all_attrs)
        instance.clean()
        return attrs


class ProductSerializer(BaseProductSerializer):
    product_type = SimpleProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ProductType.objects.all(), source="product_type"
    )
    data = DataSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data):
        data = validated_data.pop("data")

        product = Product.objects.create(**validated_data)
        product_type = product.product_type

        required_fields = list(product_type.fields.filter(is_required=True))
        data_errors = []
        for idx, entry in enumerate(data):
            field = entry["field"]
            if field.product_type != product.product_type:
                data_errors.append(
                    f"field {field.name} is not part of {product_type.name}"
                )
            elif field in required_fields:
                required_fields.remove(field)

            data_entry = Data(product=product, **entry)
            try:
                data_entry.clean()
                data_entry.save()
            except ValidationError as e:
                data_errors.append(f"Data at index {idx}: {e}")

        if required_fields:
            data_errors.append(
                f"Missing required fields: {', '.join([str(field) for field in required_fields])}"
            )

        if data_errors:
            raise serializers.ValidationError({"data": data_errors})
        return product


class DataUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Data
        exclude = ("field", "product")


class ProductUpdateSerializer(BaseProductSerializer):
    data = DataUpdateSerializer(many=True)

    class Meta:
        model = Product
        exclude = ("product_type",)

    @transaction.atomic()
    def update(self, instance, validated_data):
        data = validated_data.pop("data", None)
        product = super().update(instance, validated_data)

        if data is not None:
            data_errors = []

            current_data_ids = set(
                instance.data.values_list("id", flat=True).distinct()
            )

            seen_data_ids = set()
            for idx, data_entry in enumerate(data):
                data_id = data_entry.pop("id", None)

                if data_id in seen_data_ids:
                    data_errors.append(f"Duplicate data id: {data_id} at index {idx}")
                seen_data_ids.add(data_id)

                if data_id in current_data_ids:
                    data = Data.objects.get(pk=data_id)
                    data.value = data_entry["value"]
                    try:
                        data.clean()
                        data.save()
                    except ValidationError as e:
                        data_errors.append(f"Data at index {idx}: {e}")

                else:
                    try:
                        Data.objects.get(id=data_id)
                        data_errors.append(
                            f"Data id {data_id} at index {idx} is not part of product object"
                        )
                    except Data.DoesNotExist:
                        data_errors.append(
                            f"Data id {data_id} at index {idx} does not exist"
                        )

            if data_errors:
                raise serializers.ValidationError({"data": data_errors})

        product.refresh_from_db()

        return product
