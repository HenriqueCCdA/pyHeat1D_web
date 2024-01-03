from django.contrib import admin

from .models import Simulation


@admin.register(Simulation)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "input_file",
        "status",
    )
