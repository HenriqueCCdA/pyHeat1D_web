from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from pyheat1d_web.accounts.models import CustomUser as User
from pyheat1d_web.core.models import Simulation


class SimulationInline(admin.StackedInline):
    model = Simulation
    fields = ["tag"]
    readonly_fields = ["tag"]
    extra = 0


class UserAdmin(UserAdmin):
    inlines = [SimulationInline]

    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("User data"),
            {
                "fields": (
                    "name",
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "modified_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "email",
        "is_staff",
        "is_active",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )

    list_display_links = (
        "id",
        "name",
    )

    readonly_fields = (
        "id",
        "last_login",
        "created_at",
        "modified_at",
    )

    search_fields = ("name", "email")
    ordering = ("email",)

    actions = ("make_active", "make_disable")

    @admin.action(description="Mark selected entries as active")
    def make_active(self, request, queryset):
        queryset.filter(is_staff=False).update(is_active=True)

    @admin.action(description="Mark selected entries as disable")
    def make_disable(self, request, queryset):
        queryset.filter(is_staff=False).update(is_active=False)


admin.site.register(User, UserAdmin)
