from django.contrib import admin

from .models import Simulation


@admin.register(Simulation)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "input_file",
        "status",
        "created_at",
        "modified_at",
    )

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
    )
