from django.contrib import admin

from ..models import Tag, TagType


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type__name",)
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("type")


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
