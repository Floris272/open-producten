from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Neighbourhood, Organisation, OrganisationType


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type__name", "city")
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        (
            None,
            {"fields": ("name", "type", "logo", "neighbourhood")},
        ),
        (_("Contact"), {"fields": ("email", "phone_number")}),
        (
            _("Address"),
            {"fields": ("street", "house_number", "postcode", "city")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("neighbourhood", "type")


@admin.register(OrganisationType)
class OrganisationTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Neighbourhood)
class NeighbourhoodAmin(admin.ModelAdmin):
    list_display = ("name",)
