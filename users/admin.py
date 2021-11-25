from django.contrib import admin

from .models import ChangePasswordKey, User


def false_used(modeladmin, request, queryset):
    queryset.update(used=False)

@admin.display(description='Email')
def email(obj):
    return obj.user.email

@admin.display(description='Name')
def name(obj):
    return obj.user.full_name

class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    list_per_page = 50
    search_fields = ("full_name", "email")

class ChangePasswordKeyAdmin(admin.ModelAdmin):
    list_display = (email, name, "used" )
    actions = (false_used, )
    search_fields = ("user__email", )
    list_filter = ("used",)


admin.site.register(User, UserAdmin)
admin.site.register(ChangePasswordKey, ChangePasswordKeyAdmin)
