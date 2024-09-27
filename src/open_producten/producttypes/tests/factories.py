import factory.fuzzy

from ..models import (
    Category,
    Condition,
    Field,
    File,
    Link,
    Price,
    PriceOption,
    ProductType,
    Question,
    Tag,
    TagType,
    UniformProductName,
)


class UniformProductNameFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"upn {n}")
    uri = factory.Faker("url")

    class Meta:
        model = UniformProductName


class ProductTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"product type {n}")
    summary = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    published = True
    uniform_product_name = factory.SubFactory(UniformProductNameFactory)

    class Meta:
        model = ProductType


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"category {n}")
    description = factory.Faker("sentence")
    published = True

    class Meta:
        model = Category

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """For now factory creates only root categories"""
        return Category.add_root(**kwargs)


class TagTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"tag type {n}")

    class Meta:
        model = TagType


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"tag {n}")
    type = factory.SubFactory(TagTypeFactory)

    class Meta:
        model = Tag


class ConditionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    question = factory.Faker("word")
    positive_text = factory.Faker("sentence")
    negative_text = factory.Faker("sentence")

    class Meta:
        model = Condition


class QuestionFactory(factory.django.DjangoModelFactory):
    question = factory.Faker("sentence")
    answer = factory.Faker("text")

    class Meta:
        model = Question


class PriceFactory(factory.django.DjangoModelFactory):
    valid_from = factory.Faker("date")
    product_type = factory.SubFactory(ProductTypeFactory)

    class Meta:
        model = Price


class PriceOptionFactory(factory.django.DjangoModelFactory):
    description = factory.Faker("sentence")
    amount = factory.fuzzy.FuzzyDecimal(1, 10)

    class Meta:
        model = PriceOption


class FieldFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"field {n}")
    description = factory.Faker("sentence")
    product_type = factory.SubFactory(ProductTypeFactory)

    class Meta:
        model = Field


class FileFactory(factory.django.DjangoModelFactory):
    product_type = factory.SubFactory(ProductTypeFactory)
    file = factory.django.FileField(filename="test_file.txt")

    class Meta:
        model = File


class LinkFactory(factory.django.DjangoModelFactory):
    product_type = factory.SubFactory(ProductTypeFactory)
    name = factory.Sequence(lambda n: f"link {n}")
    url = factory.Faker("url")

    class Meta:
        model = Link
