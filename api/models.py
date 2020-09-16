from django.db import models
from django.contrib import admin
from reversion.admin import VersionAdmin
import uuid


class QRCode(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    form_url = models.URLField(blank=True, default='', help_text='links to a form')
    redirect_url = models.URLField(blank=True, default='', help_text='redirect to external page')
    basic_info = models.CharField(max_length=1000, help_text='short information about device')


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    pass
