from django.db import models
import uuid


class QRCode(models.Model):
    title = models.CharField(blank=True, default='', max_length=100)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=True
    )

    form_url = models.URLField(
        blank=True, default='', help_text='links to a form')
    redirect_url = models.URLField(
        blank=True, default='', help_text='redirect to external page')
    basic_info = models.TextField(blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
