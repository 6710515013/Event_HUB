
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Event Hub Information", {
            "fields": ("role", "student_id"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Event Hub Information", {
            "fields": ("role", "student_id"),
        }),
    )

    list_display = (
        "username",
        "email",
        "role",
        "student_id",
        "is_staff",
    )
