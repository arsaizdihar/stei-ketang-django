from django.contrib import admin

from .models import ChangePasswordKey, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    list_per_page = 50
    search_fields = ("full_name", "email")


admin.site.register(User, UserAdmin)
admin.site.register(ChangePasswordKey)
