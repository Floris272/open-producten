from django.db import models
from django.utils.translation import gettext_lazy as _

from open_producten.utils.models import BaseModel


class UniformProductName(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        help_text=_("Uniform product name"),
        unique=True,
    )

    uri = models.URLField(
        verbose_name=_("Uri"),
        help_text=_("Uri to the upn definition."),
        unique=True,
    )
    is_deleted = models.BooleanField(
        _("Is deleted"),
        help_text=_("defines if the upn definition is deleted."),
        default=False,
    )

    class Meta:
        verbose_name = _("Uniform product name")
        verbose_name_plural = _("Uniform product names")

    def __str__(self):
        return self.name
