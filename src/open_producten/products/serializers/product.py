from django.core.exceptions import ValidationError
from rest_framework import serializers

from open_producten.products.models import Data, Product
from open_producten.producttypes.models import Field, ProductType
from open_producten.producttypes.serializers.children import FieldSerializer
from open_producten.producttypes.serializers.producttype import (
    UniformProductNameSerializer,
)


class DataSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=True)
    field_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Field.objects.all(), source="field"
    )
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Data
        fields = "__all__"


class SimpleProductTypeSerializer(serializers.ModelSerializer):
    uniform_product_name = UniformProductNameSerializer()

    class Meta:
        model = ProductType
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_type = SimpleProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ProductType.objects.all(), source="product_type"
    )
    data = DataSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    def _validate_product(self, product, errors):
        try:
            product.clean()
        except ValidationError:
            errors.append("")

    def create(self, validated_data):
        data = validated_data.pop("data")

        product = Product.objects.create(**validated_data)

        product_type = product.product_type

        required_fields = list(product_type.fields.filter(is_required=True).all())
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
            except ValidationError as e:
                data_errors.append(f"Data at index {idx}: {e}")
            data_entry.save()

        if required_fields:
            data_errors.append(
                f"Missing required fields: {', '.join([str(field) for field in required_fields])}"
            )

        if data_errors:
            raise serializers.ValidationError({"data": data_errors})
        elif not product.bsn and not product.kvk:  # TODO
            raise serializers.ValidationError(
                "A product must be linked to a bsn or kvk number (or both)"
            )

        return product

    def update(self, instance, validated_data):
        data = validated_data.pop("data", None)
        product = super().update(instance, validated_data)
        data_errors = []

        if data is not None:
            current_data_ids = set(instance.data.values_list("id", flat=True))
            seen_data_ids = set()
            for idx, data_entry in enumerate(data):
                data_id = data_entry.pop("id", None)

                if data_id is None:
                    data_entry = Data(product=product, **data_entry)

                    try:
                        data_entry.clean()
                    except ValidationError as e:
                        data_errors.append(f"Data id {data_id} at index {idx}: {e}")
                    data_entry.save()

                elif data_id in current_data_ids:

                    if data_id in seen_data_ids:
                        data_errors.append(
                            f"Duplicate data id: {data_id} at index {idx}"
                        )

                    seen_data_ids.add(data_id)

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
            elif not product.bsn and not product.kvk:  # TODO
                raise serializers.ValidationError(
                    "A product must be linked to a bsn or kvk number (or both)"
                )

            Data.objects.filter(id__in=(current_data_ids - seen_data_ids)).delete()

        return product
