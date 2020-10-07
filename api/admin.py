from django.contrib import admin
from reversion.admin import VersionAdmin

from api.models import Department, QRCode
from api.filters import HasRedirectFilter, HasBasicInfoFilter, HasFormFilter


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    list_display = ('title', 'department', 'uuid')
    list_filter = (HasRedirectFilter, HasFormFilter,
                   HasBasicInfoFilter, ('department', admin.RelatedOnlyFieldListFilter))


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = 'Qr Gent Administration'
admin.site.site_title = 'Qr Gent admin'
admin.site.site_url = '/code'
