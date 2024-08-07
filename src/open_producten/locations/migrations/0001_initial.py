# Generated by Django 4.2.13 on 2024-09-04 09:37

import django.db.models.deletion
from django.db import migrations, models

import open_producten.utils.validators
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="Name"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="Email address"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=15,
                        validators=[
                            open_producten.utils.validators.validate_phone_number
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "street",
                    models.CharField(
                        blank=True,
                        help_text="Address street",
                        max_length=250,
                        verbose_name="street",
                    ),
                ),
                (
                    "house_number",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="house number"
                    ),
                ),
                (
                    "postcode",
                    models.CharField(
                        help_text="Address postcode",
                        max_length=7,
                        validators=[
                            open_producten.utils.validators.CustomRegexValidator(
                                message="Invalid postal code.",
                                regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                            )
                        ],
                        verbose_name="postcode",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        help_text="Address city", max_length=250, verbose_name="city"
                    ),
                ),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.CreateModel(
            name="Neighbourhood",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Neighbourhood name",
                        max_length=100,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Neighbourhood",
                "verbose_name_plural": "Neighbourhoods",
            },
        ),
        migrations.CreateModel(
            name="OrganisationType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Organisation type",
                        max_length=100,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organisation type",
                "verbose_name_plural": "Organisation types",
            },
        ),
        migrations.CreateModel(
            name="Organisation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="Name"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="Email address"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=15,
                        validators=[
                            open_producten.utils.validators.validate_phone_number
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "street",
                    models.CharField(
                        blank=True,
                        help_text="Address street",
                        max_length=250,
                        verbose_name="street",
                    ),
                ),
                (
                    "house_number",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="house number"
                    ),
                ),
                (
                    "postcode",
                    models.CharField(
                        help_text="Address postcode",
                        max_length=7,
                        validators=[
                            open_producten.utils.validators.CustomRegexValidator(
                                message="Invalid postal code.",
                                regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                            )
                        ],
                        verbose_name="postcode",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        help_text="Address city", max_length=250, verbose_name="city"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Slug of the organisation",
                        max_length=100,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        help_text="Logo of the organisation",
                        null=True,
                        upload_to="",
                        verbose_name="Logo",
                    ),
                ),
                (
                    "neighbourhood",
                    models.ForeignKey(
                        blank=True,
                        help_text="The neighbourhood of the organisation",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organisation",
                        to="locations.neighbourhood",
                        verbose_name="Neighbourhood",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        help_text="Organisation type",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organisations",
                        to="locations.organisationtype",
                        verbose_name="Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organisation",
                "verbose_name_plural": "Organisations",
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="First name of the contact",
                        max_length=255,
                        verbose_name="First name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Last name of the contact",
                        max_length=255,
                        verbose_name="Last name",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        help_text="The email address of the contact",
                        max_length=254,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        help_text="The phone number of the contact",
                        max_length=15,
                        validators=[
                            open_producten.utils.validators.validate_phone_number
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        help_text="The role/function of the contact",
                        max_length=100,
                        verbose_name="Rol",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        blank=True,
                        help_text="The organisation of the contact",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_contacts",
                        to="locations.organisation",
                        verbose_name="Organisation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact",
                "verbose_name_plural": "Contacts",
            },
        ),
    ]
