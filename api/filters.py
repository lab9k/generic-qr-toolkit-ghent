from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DepartmentFilter(admin.SimpleListFilter):
    title = _('on department')
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        pass

    def queryset(self, request, queryset):
        pass
