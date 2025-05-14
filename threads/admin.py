from django.contrib import admin
from threads.models import Education_Thread


@admin.register(Education_Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "name", "articul", "type_course", "is_active",
        "started_at", "ended_at",
    )
    readonly_fields = ("articul",)
    search_fields = ["name", "type_course",]

    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = "Статус"
