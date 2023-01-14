from django.contrib import admin
from .models import User
from django.contrib.admin import ModelAdmin


class UserAdmin(ModelAdmin):
    ordering = ['-last_name']
    list_display = ['last_name', 'first_name', 'email']
    list_display_links = ['last_name', 'first_name', 'email']
    list_per_page = 20
    search_fields = ['last_name', 'first_name', 'email']

    fieldsets = [('User information', {'fields': ['first_name', 'last_name', 'email', 'username', 'password']}),
                 ('Permissions', {'fields': ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser']}),
                 ('Account information', {'fields': ['last_login', 'date_joined']})]
    readonly_fields = ['date_joined', 'last_login']


admin.site.register(User, UserAdmin)
