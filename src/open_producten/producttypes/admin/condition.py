from django.contrib import admin

from ..models import Condition


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "question",
        "display_product_types",
    )
    list_filter = ("product_types__name",)
    search_fields = ("name",)

    @admin.display(description="Product types")
    def display_product_types(self, obj):
        return ", ".join(p.name for p in obj.product_types.all())
