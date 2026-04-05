from django.contrib import admin
from orm.models.user_trainer import UserTrainer

from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.register(UserTrainer)

@admin.register(UserTrainer)
class UserTrainerAdmin(UserAdmin):
    # Show custom field when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("is_trainer",)}),
    )

    # Show custom field when creating a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("is_trainer",)}),
    )