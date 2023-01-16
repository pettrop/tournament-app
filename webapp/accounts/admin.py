from django.contrib import admin
from .models import User, Profile
from django.contrib.admin import ModelAdmin


class UserAdmin(ModelAdmin):
    ordering = ['-last_name']
    list_display = ['last_name', 'first_name', 'email', 'pk']
    list_display_links = ['last_name', 'first_name', 'email']
    list_per_page = 20
    search_fields = ['last_name', 'first_name', 'email']
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = [('User information', {'fields': ['first_name', 'last_name', 'email', 'username', ]}),  # password excluded
                 ('Permissions', {'fields': ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser']}),
                 ('Account information', {'fields': ['last_login', 'date_joined']})]
    readonly_fields = ['date_joined', 'last_login']


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
