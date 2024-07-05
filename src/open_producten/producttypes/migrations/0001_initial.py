# Generated by Django 4.2.13 on 2024-07-05 14:46

import datetime
from decimal import Decimal
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Condition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the object is accessible with the api.",
                        verbose_name="Published",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date the object was created. This field is automatically set.",
                        verbose_name="Created on",
                    ),
                ),
                (
                    "updated_on",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date when the object was last changed. This field is automatically set.",
                        verbose_name="Updated on",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Short name of the condition",
                        max_length=100,
                        verbose_name="Name",
                    ),
                ),
                (
                    "question",
                    models.TextField(
                        help_text="Question used in the question-answer game",
                        verbose_name="Question",
                    ),
                ),
                (
                    "positive_text",
                    models.TextField(
                        help_text="Description how to meet the condition",
                        verbose_name="Positive text",
                    ),
                ),
                (
                    "negative_text",
                    models.TextField(
                        help_text="Description how not to meet the condition",
                        verbose_name="Negative text",
                    ),
                ),
                (
                    "rule",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Rule for the automated check",
                        verbose_name="Rule",
                    ),
                ),
            ],
            options={
                "verbose_name": "Condition",
                "verbose_name_plural": "Conditions",
            },
        ),
        migrations.CreateModel(
            name="Price",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        help_text="The start date for this price",
                        unique=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                datetime.date.today
                            )
                        ],
                        verbose_name="Start date",
                    ),
                ),
            ],
            options={
                "verbose_name": "Price",
                "verbose_name_plural": "Prices",
            },
        ),
        migrations.CreateModel(
            name="TagType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the tag type",
                        max_length=100,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tag type",
                "verbose_name_plural": "Tag types",
            },
        ),
        migrations.CreateModel(
            name="Upn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Uniform product name",
                        max_length=100,
                        verbose_name="Name",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        default="",
                        help_text="Url to the upn definition.",
                        verbose_name="Url",
                    ),
                ),
            ],
            options={
                "verbose_name": "Uniform product name",
                "verbose_name_plural": "Uniform product names",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the tag", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Slug of the tag",
                        max_length=100,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        help_text="Icon of the tag",
                        null=True,
                        upload_to="",
                        verbose_name="Icon",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        blank=True,
                        help_text="The related tag type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tags",
                        to="producttypes.tagtype",
                        verbose_name="Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the object is accessible with the api.",
                        verbose_name="Published",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date the object was created. This field is automatically set.",
                        verbose_name="Created on",
                    ),
                ),
                (
                    "updated_on",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date when the object was last changed. This field is automatically set.",
                        verbose_name="Updated on",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the product",
                        max_length=100,
                        verbose_name="Name",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Slug of the product",
                        max_length=100,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "summary",
                    models.TextField(
                        default="",
                        help_text="Short description of the product, limited to 300 characters.",
                        max_length=300,
                        verbose_name="Summary",
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        help_text="Icon of the product type",
                        null=True,
                        upload_to="",
                        verbose_name="Icon",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Main image of the product type",
                        null=True,
                        upload_to="",
                        verbose_name="Image",
                    ),
                ),
                (
                    "form_link",
                    models.URLField(
                        blank=True,
                        default="",
                        help_text="Action link to request the product.",
                        verbose_name="Form link",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Product content with build-in WYSIWYG editor.",
                        verbose_name="Content",
                    ),
                ),
                (
                    "keywords",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100),
                        blank=True,
                        default=list,
                        help_text="List of keywords for search",
                        size=None,
                        verbose_name="Keywords",
                    ),
                ),
                (
                    "conditions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Conditions applicable for the product type",
                        related_name="producttypes",
                        to="producttypes.condition",
                        verbose_name="Conditions",
                    ),
                ),
                (
                    "related_product_types",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Related product types to this product type",
                        to="producttypes.producttype",
                        verbose_name="Related product types",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Tags which the product is linked to",
                        related_name="products",
                        to="producttypes.tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "uniform_product_name",
                    models.ForeignKey(
                        help_text="Uniform product name defined by Dutch gov",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="producttypes",
                        to="producttypes.upn",
                        verbose_name="Uniform Product name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product type",
                "verbose_name_plural": "Product types",
            },
        ),
        migrations.CreateModel(
            name="PriceOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="The cost of the price option",
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="Price",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="The description of the option",
                        max_length=100,
                        verbose_name="Description",
                    ),
                ),
                (
                    "price",
                    models.ForeignKey(
                        help_text="The price this option belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="producttypes.price",
                    ),
                ),
            ],
            options={
                "verbose_name": "Price option",
                "verbose_name_plural": "Price options",
            },
        ),
        migrations.AddField(
            model_name="price",
            name="product_type",
            field=models.ForeignKey(
                help_text="The product type that this price belongs to",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prices",
                to="producttypes.producttype",
            ),
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name for the link",
                        max_length=100,
                        verbose_name="Name",
                    ),
                ),
                (
                    "url",
                    models.URLField(help_text="Url of the link", verbose_name="Url"),
                ),
                (
                    "product_type",
                    models.ForeignKey(
                        help_text="Related product type",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        to="producttypes.producttype",
                        verbose_name="Product type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product type link",
                "verbose_name_plural": "Product type links",
            },
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="", verbose_name="File")),
                (
                    "product_type",
                    models.ForeignKey(
                        help_text="Related product type",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="producttypes.producttype",
                        verbose_name="Product type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product file",
                "verbose_name_plural": "Product files",
            },
        ),
        migrations.CreateModel(
            name="Field",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("bsn", "Bsn"),
                            ("checkbox", "Checkbox"),
                            ("Cosign", "Cosign"),
                            ("currency", "Currency"),
                            ("date", "Date"),
                            ("datetime", "Datetime"),
                            ("email", "Email"),
                            ("file", "File"),
                            ("iban", "Iban"),
                            ("licenseplate", "License Plate"),
                            ("map", "Map"),
                            ("number", "Number"),
                            ("password", "Password"),
                            ("phoneNumber", "Phone Number"),
                            ("postcode", "Postcode"),
                            ("radio", "Radio"),
                            ("select", "Select"),
                            ("selectBoxes", "Select Boxes"),
                            ("signature", "Signature"),
                            ("textfield", "Textfield"),
                            ("time", "Time"),
                        ],
                        default="textfield",
                        help_text="The formio type of the field",
                        max_length=255,
                        verbose_name="Type",
                    ),
                ),
                ("is_required", models.BooleanField(default=False)),
                (
                    "choices",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100),
                        blank=True,
                        default=list,
                        help_text="The Choices that can be selected in the form",
                        null=True,
                        size=None,
                        verbose_name="Choices",
                    ),
                ),
                (
                    "product_type",
                    models.ForeignKey(
                        help_text="The product that this field is part of",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="producttypes.producttype",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Field",
                "verbose_name_plural": "Fields",
            },
        ),
    ]
