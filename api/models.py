from django.db import models
import uuid

from django.db.models.fields.related import ForeignKey


class Department(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.name}'


class QRCode(models.Model):
    title = models.CharField(blank=True, default='', max_length=100)
    department = ForeignKey(
        to=Department, on_delete=models.SET_NULL, null=True)

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
