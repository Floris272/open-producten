from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from ..models import Question


@admin.register(Question)
class QuestionAdmin(OrderedModelAdmin):
    list_filter = ("category",)
    list_display = (
        "question",
        "category",
        "product_type",
    )
    search_fields = (
        "question",
        "answer",
        "category__name",
        "product_type__name",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "product_type")


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

    fields = [
        "question",
        "answer",
    ]
