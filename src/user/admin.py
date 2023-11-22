from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AdminChangeForm


# Register your models here.
class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ['full_name', 'username', 'email']
    ordering = ['created']
    list_display = ['username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']


    form = AdminChangeForm

    fieldsets = (
        (None, {'fields': (['email'])}),
        ('Personal info', {'fields': ('full_name', 'username', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('full_name', 'username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
