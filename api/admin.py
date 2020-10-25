from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from django.urls import path

from api.models import ApiHit, Department, LinkUrl, QRCode
from api.filters import HasRedirectFilter, HasBasicInfoFilter, HasFormFilter


@admin.register(ApiHit)
class ApiHitAdmin(admin.ModelAdmin):
    readonly_fields = ('hit_date', 'action', 'code')
    list_display = ('code', 'hit_date', 'action')
    change_list_template = 'api/change_list.html'

    def get_urls(self):
        urls = super(ApiHitAdmin, self).get_urls()
        urls += [
            path('analytics', self.admin_site.admin_view(self.analytics_view))
        ]
        return urls

    def analytics_view(self, request):
        clctx = self.changelist_view(request).context_data
        clctx['title'] = 'Api Hit Analytics'
        clctx['is_nav_sidebar_enabled'] = False
        context = dict(
            self.admin_site.each_context(request),
            **clctx,
        )

        return TemplateResponse(request, template='api/apihit.analytics.html', context=context)


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

    def get_queryset(self, request):
        qs = super(QRCodeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(department=request.user.department)

    def get_model_perms(self, request):
        return super(QRCodeAdmin, self).get_model_perms(request)

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
