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

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_trainer', 'is_staff', 'display_groups')
    def display_groups(self, obj):
        """
        Returns a comma-separated list of group names for the user.
        """
        return ", ".join([group.name for group in obj.groups.all()])
    
    display_groups.short_description = 'Groups'  # Column header name

    
    list_per_page = 6