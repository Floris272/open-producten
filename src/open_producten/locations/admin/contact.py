from django.contrib import admin

from ..models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("organisation", "last_name", "first_name")
    list_filter = ("organisation",)
    search_fields = ("first_name", "last_name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("organisation")
