from django.contrib import admin
from api.models import QRCode
from reversion.admin import VersionAdmin


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    list_display = ('title', 'uuid')
