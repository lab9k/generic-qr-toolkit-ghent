from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin

from api.models import ApiHit, Department, LinkUrl, QRCode
from api.filters import HasRedirectFilter, HasBasicInfoFilter, HasFormFilter


@admin.register(ApiHit)
class ApiHitAdmin(admin.ModelAdmin):
    readonly_fields = ('hit_date', 'action', 'code')
    list_display = ('code', 'hit_date', 'action')


class LinkUrlInline(admin.StackedInline):
    model = LinkUrl
    extra = 1


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    list_display = ('title', 'department',
                    'get_code_url', 'get_code_image_url')
    list_filter = (HasRedirectFilter, HasFormFilter,
                   HasBasicInfoFilter, ('department', admin.RelatedOnlyFieldListFilter))
    search_fields = ('title', 'department__name')
    inlines = [LinkUrlInline]

    def get_code_image_url(self, obj):
        return mark_safe(f'<span><a href="/code/{obj.uuid}">/code/{obj.uuid}</a></span>')

    def get_code_url(self, obj):
        return mark_safe(f'<span><a href="/{obj.uuid}">/{obj.uuid}</a></span>')

    get_code_image_url.short_description = 'Code image'
    get_code_url.short_description = 'Code url'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = 'Qr Gent Administration'
admin.site.site_title = 'Qr Gent admin'
admin.site.site_url = '/code'
