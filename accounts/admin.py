from accounts.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

UserAdmin.list_display += ('department',)
UserAdmin.list_filter += ('department',)
UserAdmin.fieldsets = (
    (None, {'fields': ('username', 'password', 'department')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
)
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2', 'department'),
    }),
)

admin.site.register(User, UserAdmin)
