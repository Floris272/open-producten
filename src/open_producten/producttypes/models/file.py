from django.db import models
from django.utils.translation import gettext_lazy as _

from open_producten.core.models import BaseModel

from .producttype import ProductType


class File(BaseModel):
    product_type = models.ForeignKey(
        ProductType,
        verbose_name=_("Product type"),
        related_name="files",
        on_delete=models.CASCADE,
        help_text=_("Related product type"),
    )
    file = models.FileField(verbose_name=_("File"))

    class Meta:
        verbose_name = _("Product file")
        verbose_name_plural = _("Product files")

    def __str__(self):
        return self.file.name
