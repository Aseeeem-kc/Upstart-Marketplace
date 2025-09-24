
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_verified', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_editable = ('is_active', 'is_verified')
    readonly_fields = ('email_token', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('is_verified', 'email_token')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)