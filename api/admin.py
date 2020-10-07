from django.contrib import admin
from reversion.admin import VersionAdmin

from api.models import QRCode
from api.filters import HasRedirectFilter, HasBasicInfoFilter, HasFormFilter


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    list_display = ('title', 'uuid')
    list_filter = (HasRedirectFilter, HasFormFilter, HasBasicInfoFilter)
