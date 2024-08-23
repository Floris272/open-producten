from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from localflavor.generic.validators import IBANValidator
from localflavor.nl.validators import NLLicensePlateFieldValidator

from open_producten.producttypes.models import Field, FieldTypes
from open_producten.utils.models import BaseModel
from open_producten.utils.validators import validate_postal_code

from .product import Product
from .validators import (
    validate_bsn,
    validate_checkbox,
    validate_datetime_format,
    validate_radio,
    validate_regex,
    validate_select,
    validate_select_boxes,
)


class Data(BaseModel):
    field = models.ForeignKey(
        Field,
        verbose_name=_("Field"),
        on_delete=models.CASCADE,
        help_text=_("The field that this data belongs to"),
        related_name="data",
    )
    value = models.CharField(_("Value"), help_text=_("The value of the field"))

    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.RESTRICT,
        help_text=_("The product that this data belongs to"),
        related_name="data",
    )

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Data")

    def __str__(self):
        return f"{self.field.name} {self.product_type.name}"

    @property
    def product_type(self):
        return self.field.product_type

    PARSERS = {
        FieldTypes.NUMBER: float,
        FieldTypes.CHECKBOX: lambda value: value.lower() == "true",
        FieldTypes.DATE: lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        FieldTypes.DATETIME: lambda value: datetime.strptime(
            value, "%Y-%m-%dT%H:%M:%S%z"
        ),
        FieldTypes.TIME: lambda value: datetime.strptime(value, "%H:%M:%S").time(),
        FieldTypes.MAP: lambda value: value.split(","),
        FieldTypes.SELECT: lambda value: value.split(","),
    }

    CLEANERS = {
        FieldTypes.BSN: validate_bsn,
        FieldTypes.CHECKBOX: validate_checkbox,
        FieldTypes.COSIGN: lambda value: validate_regex(
            value, r"^.+@.+\..+$", FieldTypes.EMAIL
        ),
        FieldTypes.CURRENCY: lambda value: validate_regex(
            value, r"^\d+,?\d{0,2}$", FieldTypes.CURRENCY
        ),
        FieldTypes.DATE: lambda value: validate_datetime_format(
            value, "%Y-%m-%d", FieldTypes.DATE
        ),
        FieldTypes.DATETIME: lambda value: validate_datetime_format(
            value, "%Y-%m-%dT%H:%M:%S%z", FieldTypes.DATETIME
        ),
        FieldTypes.EMAIL: lambda value: validate_regex(
            value, r"^.+@.+\..+$", FieldTypes.EMAIL
        ),
        FieldTypes.IBAN: IBANValidator(),
        FieldTypes.LICENSE_PLATE: NLLicensePlateFieldValidator(),
        FieldTypes.MAP: lambda value: validate_regex(
            value, r"^\d+\.?\d*,\d+\.?\d*$", FieldTypes.MAP
        ),
        FieldTypes.NUMBER: lambda value: validate_regex(
            value, r"^\d+\.?\d*$", FieldTypes.NUMBER
        ),
        FieldTypes.PHONE_NUMBER: lambda value: validate_regex(
            value, r"^[+0-9][- 0-9]+$", FieldTypes.PHONE_NUMBER
        ),
        FieldTypes.POSTCODE: validate_postal_code,
        FieldTypes.SIGNATURE: lambda value: validate_regex(
            value, r"^data:image/png;base64,.*$", FieldTypes.SIGNATURE
        ),
        FieldTypes.TIME: lambda value: validate_datetime_format(
            value, "%H:%M:%S", FieldTypes.TIME
        ),
    }

    CHOICE_CLEANERS = {
        FieldTypes.RADIO: validate_radio,
        FieldTypes.SELECT: validate_select,
        FieldTypes.SELECT_BOXES: validate_select_boxes,
    }

    def format(self):
        if self.field.type in self.PARSERS:
            return self.PARSERS[self.field.type](self.value)

    def clean(self):
        if self.field.type in self.CLEANERS:
            self.CLEANERS[self.field.type](self.value)

        elif self.field.type in self.CHOICE_CLEANERS:
            self.CHOICE_CLEANERS[self.field.type](self.value, self.field.choices)
