from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import User, Profile


class UserAdmin(ModelAdmin):
    ordering = ['last_name', 'first_name']
    list_display = ['last_name', 'first_name', 'email',]
    list_display_links = ['last_name', 'first_name', 'email']
    list_per_page = 20
    search_fields = ['last_name', 'first_name', 'email']
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = [('User information', {'fields': ['first_name', 'last_name', 'email',]}),  # password & username excluded
                 ('Permissions', {'fields': ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser']}),
                 ('Account information', {'fields': ['last_login', 'date_joined']})]
    readonly_fields = ['date_joined', 'last_login']


class ProfileAdmin(ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'club', 'phone']
    list_display_links = ['user']
    list_per_page = 20
    search_fields = ['user', 'club', 'phone']

    fieldsets = [('Profile information', {'fields': ['user', 'phone', 'club']})]
    readonly_fields = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
