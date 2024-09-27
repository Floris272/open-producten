from django.contrib import admin

from ..models import UniformProductName


@admin.register(UniformProductName)
class UniformProductNameAdmin(admin.ModelAdmin):
    list_display = ("name", "uri", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("name", "uri")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
